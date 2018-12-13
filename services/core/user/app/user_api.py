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
    user_response = requests.post("http://user-access:5200/v1/users", json=user)

    return make_response(json.dumps(user_response.json()), user_response.status_code)

def delete_user(id):
    user_response = requests.delete("http://user-access:5200/v1/users/{}".format(id))
    return make_response(json.dumps(user_response.json()), user_response.status_code)

def get_user(id):
    user_response = requests.get("http://user-access:5200/v1/users/{}".format(id))
    user = user_response.json()
    user["password"] = ""
    return make_response(json.dumps(user), user_response.status_code)

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

def authorize_user():
    access_token = request.json["access_token"]
    #Fra data access får jeg enten en 200 for at token eksisterer, eller 404 for at den ikke gør
    response = requests.get("http://user-acess:5200/v1/users/{}".format(access_token)).json()
    #hvis 200, send 200 #ellers hvis 404, send 401 tilbage
    if response.status_code == 404:
        return 401
    else:
        return reponse


#Tag et device id og et device liste og et user id
#Check device id not in list
#if true call user/id med patch request. Den skal have en operation, og en entry i otherdevice.
#Operation og device skal i en json body.

#MEYER: LAV ALT TIL 200 OG SEND OBJEKTET MED


