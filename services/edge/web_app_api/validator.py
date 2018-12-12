import re


# This function is used when an input is required to be alphanumeric, such as with usernames and passwords. This
# Ensures that code cannot be injected into queries.
def is_alphanumeric(string):
    r = re.compile('([A-Z]|[a-z]|[1-9])\w+')

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


def is_only_expected_data(recieved_dictionary, expected_dictionary):

    for key in expected_dictionary:
        if key not in recieved_dictionary.keys():
            return "Expected: {" + ', '.join(expected_dictionary) + "}\nGot: {" + ', '.join(recieved_dictionary.keys()) + "}\nDidnt find: " + key

    for key in list(recieved_dictionary.keys()):
        if key not in expected_dictionary:
            return "Expected: {" + ', '.join(expected_dictionary) + "}\nGot: {" + ', '.join(recieved_dictionary.keys()) + "}\nDidnt expect: " + key
    return ""


def validate_request_body(request):
    result = is_only_expected_data(request.json, ["accessToken", "data"])
    if result != "":
        return result


    return is_alphanumeric(request.json["accessToken"])

def validate_users_request(request):
    validate_body_result = validate_request_body(request)

    if validate_body_result != "":
        return validate_body_result


    result = is_only_expected_data(request.json["data"], ["username", "password"])
    if result != "":
        return result

    expected_fields = ["username", "password"]

    for field in expected_fields:
        result = is_alphanumeric(request.json["data"][field])
        if result != "":
            return result

    return ""


def validate_devices_request(request):

    validate_body_result = validate_request_body(request)

    if validate_body_result != "":
        return validate_body_result

    result = is_only_expected_data(request.json["data"], ["prettyName"])
    if result != "":
        return result

    expected_fields = ["prettyName"]

    for field in expected_fields:
        result = is_alphanumeric_or_whitespace(request.json["data"][field])
        if result != "":
            return result

    return ""



def validate_sensors_request(request):

    validate_body_result = validate_request_body(request)

    if validate_body_result != "":
        return validate_body_result

    result = is_only_expected_data(request.json["data"], ["prettyName", "public", "accessTokens"])
    if result != "":
        return result


    public = request.json.data["public"]
    accesstokens = request.json["data"]["accessTokens"]

    for token in accesstokens:
        if(is_alphanumeric(token) == False):
            return False

    if isinstance(public, bool) == False:
        return "\"public\" must be of type bool"

    expected_fields = ["prettyName"]

    for field in expected_fields:
        result = is_alphanumeric_or_whitespace(request.json["data"][field])
        if result != "":
            return result

    return ""


def validate_actions_request(request):
    result = is_only_expected_data(request.json["data"], ["prettyName", "public", "accessTokens"])
    if result != "":
        return result


    public = request.json["data"]["public"]
    accesstokens = request.json["dataaccessTokens"]

    for token in accesstokens:
        if(is_alphanumeric(token) == False):
            return False

    if isinstance(public, bool) == False:
        return "\"public\" must be of type bool"

    expected_fields = ["prettyName"]

    for field in expected_fields:
        result = is_alphanumeric_or_whitespace(request.json["data"][field])
        if result != "":
            return result

    return ""