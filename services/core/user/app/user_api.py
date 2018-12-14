from flask import jsonify, request, json, make_response
from coapthon.client.helperclient import HelperClient
import requests, hashlib, uuid


### Data Access Endpoints

def add_user():
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
    user = requests.get("http://user-access:5200/v1/users/{}".format(id)).json()
    if "devices" in user:
        for deviceid in user["devices"]:
            requests.delete("http://device-service:5400/v1/devices/{}/".format(deviceid))
    user_response = requests.delete("http://user-access:5200/v1/users/{}".format(id))
    return make_response(user_response.content, user_response.status_code)

def get_user(id):
    user_response = requests.get("http://user-access:5200/v1/users/{}".format(id))
    user = user_response.json()
    user["password"] = ""
    return make_response(json.dumps(user), user_response.status_code)

def get_user_id(username):
    user_response = requests.get("http://user-access:5200/v1/users/getId/{}".format(username))
    return make_response(user_response.content, user_response.status_code)

def patch_user(id):
    user_patch = request.json
    if 'password' in user_patch:
        user_patch["password"] = hash_password(user_patch["password"])
    user_response = requests.patch("http://user-access:5200/v1/users/{}".format(id), json=user_patch)
    user = user_response.json()
    user["password"] = ""
    return make_response(json.dumps(user), user_response.status_code)

def authenticate_user():
    login = {
        "username" : request.json["username"],
        "password" : request.json["password"]
    }
    userId = requests.get("http://user-access:5200/v1/users/getId/{}".format(login["username"])).text
    userId = userId.replace('\"', '').rstrip()
    user_response = requests.get("http://user-access:5200/v1/users/{}".format(userId))
    user = user_response.json()
    if check_password(login["password"], user["password"]):
        user["password"] = ""
        return make_response(json.dumps(user), user_response.status_code)
    else:
        return make_response(401)

def hash_password(password):
    foo = uuid.uuid4().hex
    return hashlib.sha256(foo.encode() + password.encode()).hexdigest() + ':' + foo

def check_password(userPassword, hashedPassword):
    password, foo = hashedPassword.split(':')
    return password == hashlib.sha256(foo.encode() + userPassword.encode()).hexdigest()

def authorize_user(id):
    access_token = request.json["accessToken"]
    #Fra data access får jeg enten en 200 for at token eksisterer, eller 404 for at den ikke gør
    response = requests.get("http://user-access:5200/v1/users/{}".format(access_token))
    user = response.json()
    #hvis 200, send 200 #ellers hvis 404, send 401 tilbage
    if response.status_code == 404:
        return make_response(json.dumps({"error": "user not found."}), 404)
    elif user["_id"] != id:
        return make_response(json.dumps({"error": "not authorized"}), 401)
    else:
        return make_response(response.content, 200)


