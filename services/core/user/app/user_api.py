from flask import jsonify, request, json, make_response
import requests, hashlib, uuid

users = []
user1 = {
    "username" : "testuser",
    "password" : "testpass",
    "access_token" : "cooltoken"
}
users.append(user1)

### Data Access Endpoints

def add_user():
    user = {
        "username" : request.json["username"],
        "password" : hashPassword(request.json["password"]),
        "access_token" : request.json["access_token"]
    }
    r = requests.post("http://user-access:5200/v1/users", json=user)
    return jsonify({'response': r.json()})

def delete_user(id):
    r = requests.delete("http://user-access:5200/v1/users/{}".format(id))
    return r.text

def get_user(id):
    r = requests.get("http://user-access:5200/v1/users/{}".format(id))
    r["password"] = None
    return r.json()

def get_user_id(username):
    r = requests.get("http://user-access:5200/v1/users/getId/{}".format(username))
    return r.text

def patch_user(id):
    r = requests.patch("http://user-access:5200/v1/users/{}".format(id), json=request.json)

def authenticate_user():
    login = {
        "username" : request.json["username"],
        "password" : request.json["password"]
    }
    userId = requests.get("http://user-access:5200/v1/users/getId/{}".format(login["username"])).text
    userId = userId.replace('\"', '').rstrip()
    user = requests.get("http://user-access:5200/v1/users/{}".format(userId)).json()
    if checkPassword(login["password"], user["password"]):
        user["password"] = None
        return user
    else:
        return make_response(401)

def hashPassword(password):
    foo = uuid.uuid4().hex
    return hashlib.sha256(foo.encode() + password.encode()).hexdigest() + ':' + foo

def checkPassword(userPassword, hashedPassword):
    password, foo = hashedPassword.split(':')
    return password == hashlib.sha256(foo.encode() + userPassword.encode()).hexdigest()

#Tag et device id og et device liste og et user id
#Check device id not in list
#if true call user/id med patch request. Den skal have en operation, og en entry i otherdevice.
#Operation og device skal i en json body.

