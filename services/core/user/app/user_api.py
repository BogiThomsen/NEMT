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
    random = uuid.uuid4().hex
    access_token = hashlib.sha224(random.encode()).hexdigest()
    user = {
        "username" : request.json["username"],
        "password" : hash_password(request.json["password"]),
        "access_token" : access_token
    }
    user_response = requests.post("http://user-access:5200/v1/users", json=user)
    user = user_response.json()
    user["password"] = ""
    return make_response(json.dumps(user), user_response.status_code)
    
def delete_user(id):
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
    user_response = requests.patch("http://user-access:5200/v1/users/{}".format(id), json=request.json)
    return make_response(user_response.content, user_response,status_code)

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
    access_token = request.json["access_token"]
    #Fra data access får jeg enten en 200 for at token eksisterer, eller 404 for at den ikke gør
    response = requests.get("http://user-acess:5200/v1/users/{}".format(access_token))
    user = response.json()
    #hvis 200, send 200 #ellers hvis 404, send 401 tilbage
    if response.status_code == 404:
        return make_response(json.dumps({"error": "not authorized from db"}), 401)
    elif user["_id"] != userid:
        return make_response(json.dumps({"error": "not authorized id"}), 401)
    else:
        return make_response(response.content, 200)


#Tag et device id og et device liste og et user id
#Check device id not in list
#if true call user/id med patch request. Den skal have en operation, og en entry i otherdevice.
#Operation og device skal i en json body.

#MEYER: LAV ALT TIL 200 OG SEND OBJEKTET MED


