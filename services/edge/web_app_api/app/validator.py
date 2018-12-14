# This function is used when an input is required to be alphanumeric, such as with usernames and passwords. This
# Ensures that code cannot be injected into queries.
import re

from pip._internal import req


def is_alphanumeric(string):
    r = re.compile('^[\w]+$')

    if r.match(string) is None:
        return string + " is not alphanumeric."
    elif r.match(string).group() == string:
        return ""
    else:
        return "Not allowed: \"" + string.replace(r.match(string).group(), "") + "\" in " + "\"" + string + "\""


def is_alphanumeric_or_whitespace(string):
    r = re.compile('^[\w ]+$')

    if r.match(string) is None:
        return string + " is not alphanumeric, nor space."
    elif r.match(string).group() == string:
        return ""
    else:
        return "Not allowed: \"" + string.replace(r.match(string).group(), "") + "\" in " + "\"" + string + "\""

def data_is_any_of(recieved_dictionary, expected_dictionary):
    for key in list(recieved_dictionary.keys()):
        if key not in expected_dictionary:
            return "Expected any of: {" + ', '.join(expected_dictionary) + "}\nGot: {" + ', '.join(recieved_dictionary.keys()) + "}\nDidnt expect: " + key
    return ""


def is_only_expected_data(recieved_dictionary, expected_dictionary, optional_dictionary = []):

    for key in expected_dictionary:
        if key not in recieved_dictionary.keys():
            return "Expected: {" + ', '.join(expected_dictionary) + "}\nGot: {" + ', '.join(recieved_dictionary.keys()) + "}\nDidnt find: " + key

    for key in list(recieved_dictionary.keys()):
        if key not in expected_dictionary and key not in optional_dictionary:
            return "Expected: {" + ', '.join(expected_dictionary) + "}\nOptional: {" + ', '.join(optional_dictionary) + "}\nGot: {" + ', '.join(recieved_dictionary.keys()) + "}\nDidnt expect: " + key
    return ""


def validate_request_body(request):

    if request.method == "GET" or request.method == "DELETE":
        result = is_only_expected_data(request.json, ["accessToken"])
        if result != "":
            return result
        return is_alphanumeric(request.json["accessToken"])

    else:

        result = is_only_expected_data(request.json, ["accessToken", "data"])
        if result != "":
            return result
        return is_alphanumeric(request.json["accessToken"])



def validate_users_request(request):
    validate_body_result = validate_request_body(request)

    if request.method == "GET" or request.method == "DELETE":
        return validate_body_result

    elif request.method == "POST":

        result = is_only_expected_data(request.json, ["username", "password"])
        if result != "":
            return result

        expected_fields = ["username", "password"]

        for field in expected_fields:
            result = is_alphanumeric(request.json[field])
            if result != "":
                return result

        return ""

    else:
        if validate_body_result != "":
            return validate_body_result

        result = data_is_any_of(request.json["data"], ["operation", "username", "password"])
        if result != "":
            return result

        for field in list(request.json["data"].keys()):
            result = is_alphanumeric(request.json["data"][field])
            if result != "":
                return result

        return ""




def validate_devices_request(request):
    validate_body_result = validate_request_body(request)

    if request.method == "GET" or request.method == "DELETE":
        return validate_body_result


    elif request.method == "POST":
        if validate_body_result != "":
            return validate_body_result

        result = is_only_expected_data(request.json["data"], ["name", "deviceToken"], ["prettyName"])
        if result != "":
            return result

        if 'prettyName' in request.json["data"]:
            expected_fields = ["prettyName"]

            for field in expected_fields:
                result = is_alphanumeric_or_whitespace(request.json["data"][field])
                if result != "":
                    return result

        return ""


    else:
        if validate_body_result != "":
            return validate_body_result

        result = data_is_any_of(request.json["data"], ["prettyName"])
        if result != "":
            return result

        if 'prettyName' in request.json["data"]:
            expected_fields = ["prettyName"]

            for field in expected_fields:
                result = is_alphanumeric_or_whitespace(request.json["data"][field])
                if result != "":
                    return result

        return ""


def validate_sensors_request(request):

    validate_body_result = validate_request_body(request)

    if request.method == "GET" or request.method == "DELETE":
        return validate_body_result
    elif request.method == "POST":
        if validate_body_result != "":
            return validate_body_result

        result = is_only_expected_data(request.json["data"], ["prettyName", "public", "accessTokens"])
        if result != "":
            return result


        public = request.json["data"]["public"]
        accesstokens = request.json["data"]["accessTokens"]

        for token in accesstokens:
            if(is_alphanumeric(token) == False):
                return False

        if isinstance(public, bool) == False:
            return "\"public\" must be of type bool"

        if 'prettyName' in request.json["data"]:
            expected_fields = ["prettyName"]

            for field in expected_fields:
                result = is_alphanumeric_or_whitespace(request.json["data"][field])
                if result != "":
                    return result

        return ""

    else:
        if validate_body_result != "":
            return validate_body_result

        result = data_is_any_of(request.json["data"], ["operation", "prettyName", "public", "accessTokens"])
        if result != "":
            return result

        if request.json["data"]["operation"] not in ["add", "remove"]:
            return "operation should be either add or remove. it is " + request.json["data"]

        public = request.json["data"]["public"]
        accesstokens = request.json["data"]["accessTokens"]

        for token in accesstokens:
            if (is_alphanumeric(token) == False):
                return False

        if isinstance(public, bool) == False:
            return "\"public\" must be of type bool"

        if 'prettyName' in request.json["data"]:
            expected_fields = ["prettyName"]

            for field in expected_fields:
                result = is_alphanumeric_or_whitespace(request.json["data"][field])
                if result != "":
                    return result

        return ""


def validate_actions_request(request):
    validate_body_result = validate_request_body(request)

    if request.method == "GET" or request.method == "DELETE":
        return validate_body_result
    elif request.method == "POST":

        result = is_only_expected_data(request.json["data"], ["public"], ["prettyName", "accessTokens"])
        if result != "":
            return result

        public = request.json["data"]["public"]
        accesstokens = request.json["accessTokens"]

        for token in accesstokens:
            if(is_alphanumeric(token) == False):
                return False

        if isinstance(public, bool) == False:
            return "\"public\" must be of type bool"

        if 'prettyName' in request.json["data"]:
            expected_fields = ["prettyName"]

            for field in expected_fields:
                result = is_alphanumeric_or_whitespace(request.json["data"][field])
                if result != "":
                    return result

        return ""

    else:
        result = data_is_any_of(request.json["data"], ["operation", "prettyName", "public", "accessTokens"])
        if result != "":
            return result

        if request.json["data"]["operation"] not in ["add", "remove"]:
            return "operation should be either add or remove. it is " + request.json["data"]

        public = request.json["data"]["public"]
        accesstokens = request.json["dataaccessTokens"]

        for token in accesstokens:
            if (is_alphanumeric(token) == False):
                return False

        if isinstance(public, bool) == False:
            return "\"public\" must be of type bool"

        if 'prettyName' in request.json["data"]:
            expected_fields = ["prettyName"]

            for field in expected_fields:
                result = is_alphanumeric_or_whitespace(request.json["data"][field])
                if result != "":
                    return result

        return ""
