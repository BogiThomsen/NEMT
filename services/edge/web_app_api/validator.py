import re


# This function is used when an input is required to be alphanumeric, such as with usernames and passwords. This
# Ensures that code cannot be injected into queries.
def is_alphanumeric(string):
    r = re.compile('([A-Z]|[a-z]|[1-9])\w+')
    return r.match(string).group() == string


def validate_user_request(request):
    username = request.json["username"]
    password = request.json["password"]
    return is_alphanumeric(username) and is_alphanumeric(password)


def validate_device_request(request):
    prettyName = request.json["prettyName"]
    return is_alphanumeric(prettyName)


def validate_sensor_request(request):
    prettyname = request.json["prettyName"]
    public = request.json["public"]
    accesstokens = request.json["accessTokens"]

    for token in accesstokens:
        if(is_alphanumeric(token) == False):
            return False;

    return is_alphanumeric(prettyname) and isinstance(public, bool)
