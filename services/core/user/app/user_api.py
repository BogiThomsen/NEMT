from flask import jsonify, request, json, make_response
from coapthon.client.helperclient import HelperClient
import requests, hashlib, uuid


### Data Access Endpoints

def add_user():
    """Adds a user to the database, and generates an accessToken.

    Args:
        username (string): the username of the user 
        password (string): the password of the user
        

    Returns:
        the user.

    """
    random = uuid.uuid4().hex
    access_token = hashlib.sha224(random.encode()).hexdigest()
    user = {
        "username" : request.json["username"],
        "password" : hash_password(request.json["password"]),
        "accessToken" : access_token
    }
    user_response = requests.post("http://user-access:5200/v1/users", json=user)
    user = user_response.json()
    user["password"] = ""
    return make_response(json.dumps(user), user_response.status_code)
    
def delete_user(id):
    """deletes a user from the database, based on an id.

    Args:
        id (string): the id of the user 
        json (json): json object containing an accestoken
        

    Returns:
        200 response, if the user is deleted, 400 if not.

    """
    user = requests.get("http://user-access:5200/v1/users/{}".format(id)).json()
    if "devices" in user:
        for deviceid in user["devices"]:
            requests.delete("http://device-service:5400/v1/users/{0}/devices/{1}".format(id, deviceid))
    user_response = requests.delete("http://user-access:5200/v1/users/{}".format(id))
    return make_response(user_response.content, user_response.status_code)

def get_user(id):
    """Fetches a user from the database, based on an id.

    Args:
        id (string): the id of the user 
        

    Returns:
        the user as a json object.

    """
    user_response = requests.get("http://user-access:5200/v1/users/{}".format(id))
    user = user_response.json()
    user["password"] = ""
    return make_response(json.dumps(user), user_response.status_code)

def get_user_id(username):
    user_response = requests.get("http://user-access:5200/v1/users/getId/{}".format(username))
    return make_response(user_response.content, user_response.status_code)

def patch_user(id):
    """Updates user information, hashes the new password, if password change is requested.

    Args:
        id (string): the id of the user
        json (json): json object containing an accestoken and information to be updated on the user.
        

    Returns:
        the updated user.

    """
    user_patch = request.json
    if 'password' in user_patch:
        user_patch["password"] = hash_password(user_patch["password"])
    user_response = requests.patch("http://user-access:5200/v1/users/{}".format(id), json=user_patch)
    user = user_response.json()
    user["password"] = ""
    return make_response(json.dumps(user), user_response.status_code)

def authenticate_user():
    """Authenticates a user, to allow logins.

    Args:
        username (string): the username to authenticate
        password (string): the password to authenticate 
        json (json): json object containing an accestoken
        

    Returns:
        the authenticated user, or a 401 response.

    """
    login = {
        "username" : request.json["username"],
        "password" : request.json["password"]
    }
    user_response = requests.get("http://user-access:5200/v1/users/getId/{}".format(login["username"]))
    if user_response.status_code == 404:
        return make_response(user_response.content, user_response.status_code)
    else:
        user_id = user_response.text.replace('\"', '').rstrip()
        user = requests.get("http://user-access:5200/v1/users/{}".format(user_id)).json()
        if check_password(login["password"], user["password"]):
            user["password"] = ""
            return make_response(json.dumps(user), user_response.status_code)
        else:
            return make_response("Unauthorized" ,401)

def hash_password(password):
    """Hashes a password and a random string of hex characters with the sha256 algorithm.

    Args:
        password (string): the password to hash 
        

    Returns:
        the hashed password.

    """
    foo = uuid.uuid4().hex
    return hashlib.sha256(foo.encode() + password.encode()).hexdigest() + ':' + foo

def check_password(userPassword, hashedPassword):
    """Checks if the input password is correct..

    Args:
        userPassword (string): the password stored on the user
        hashedPassword (string): the password from the login form 
        

    Returns:
        True if the passwords are equal, else False

    """
    password, foo = hashedPassword.split(':')
    return password == hashlib.sha256(foo.encode() + userPassword.encode()).hexdigest()

def authorize_user(id):
    """Checks if the user is authorized to access the resources the user wants to access.

    Args:
        id (string): the id of the user
        json (json): json object containing an accestoken
        

    Returns:
        404 or 401 if the user is unauthorized, 200 if not.

    """
    access_token = request.json["accessToken"]
    #Fra data access får jeg enten en 200 for at token eksisterer, eller 404 for at den ikke gør
    response = requests.get("http://user-access:5200/v1/users/{}".format(access_token))
    user = response.json()
    #hvis 200, send 200 #ellers hvis 404, send 401 tilbage
    if response.status_code == 404:
        return make_response(json.dumps({"error": "cannot authorize, user not found."}), 404)
    elif user["_id"] != id:
        return make_response(json.dumps({"error": "not authorized"}), 401)
    else:
        return make_response(response.content, 200)


