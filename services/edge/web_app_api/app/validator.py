import re


# This function is used when an input is required to be alphanumeric, such as with usernames and passwords. This
# Ensures that code cannot be injected into queries.
def is_alphanumeric(string):
    r = re.compile('([A-Z]|[a-z]|[1-9])\w+')
    return r.match(string).group() == string


def is_alphanumeric_or_whitespace(string):
    r = re.compile('([A-Z]|[a-z]|[1-9]| )')
    return r.match(string).group() == string


def is_only_expected_data(recieved_dictionary, expected_dictionary):

    for key in expected_dictionary:
        if key not in recieved_dictionary.keys():
            return False

    for key in list(recieved_dictionary.keys()):
        if key not in expected_dictionary:
            return False
    return True


def validate_users_request(request):
    if is_only_expected_data(request.json, ["username", "password"]) == False:
        return False

    username = request.json["username"]
    password = request.json["password"]

    return is_alphanumeric(username) and is_alphanumeric(password)


def validate_devices_request(request):

    if is_only_expected_data(request.json, ["prettyName"]) == False:
        return False

    prettyName = request.json["prettyName"]

    return is_alphanumeric_or_whitespace(prettyName)


def validate_sensors_request(request):
    if is_only_expected_data(request.json, ["prettyName", "public", "accessTokens"]) == False:
        return False

    prettyname = request.json["prettyName"]
    public = request.json["public"]
    accesstokens = request.json["accessTokens"]

    for token in accesstokens:
        if(is_alphanumeric(token) == False):
            return False

    return is_alphanumeric_or_whitespace(prettyname) and isinstance(public, bool)


def validate_actions_request(request):
    if is_only_expected_data(request.json, ["prettyName", "public", "accessTokens"]) == False:
        return False

    prettyname = request.json["prettyName"]
    public = request.json["public"]
    accesstokens = request.json["accessTokens"]

    for token in accesstokens:
        if(is_alphanumeric(token) == False):
            return False

    return is_alphanumeric_or_whitespace(prettyname) and isinstance(public, bool)
