import re


# This function is used when an input is required to be alphanumeric, such as with usernames and passwords. This
# Ensures that code cannot be injected into queries.
def is_alphanumeric_or_point(string):
    r = re.compile('^[\w\.]+$')

    if r.match(string) is None:
        return string + " is not alphanumeric."
    elif r.match(string).group() == string:
        return ""
    else:
        return "Not allowed: \"" + string.replace(r.match(string).group(), "") + "\" in " + "\"" + string + "\""

def is_device_token(string):
    r = re.compile('^[\w\:]+$')

    if r.match(string) is None:
        return string + " is not alphanumeric."
    elif r.match(string).group() == string:
        return ""
    else:
        return "Not allowed: \"" + string.replace(r.match(string).group(), "") + "\" in " + "\"" + string + "\""




def validate_device_request(recieved):

    received_list = recieved.split('/')

    if len(received_list) < 2:
        return "Not enough parameters. expected at least 2. Got " + len(received_list).__str__()

    for index, key in enumerate(received_list):
        if index == 0:
            result = is_device_token(key)
            if result != "":
                return result
        else:
            result = is_alphanumeric_or_point(key)
            if result != "":
                return result

    return ""


