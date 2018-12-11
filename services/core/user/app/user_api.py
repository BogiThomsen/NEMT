from flask import jsonify, request, json
import requests

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
        "password" : request.json["password"],
        "access_token" : request.json["access_token"]
    }
    r = requests.post("http://user-access:5200/v1/users", json=user)
    return jsonify({'response': r.json()})

## Skal laves om ift. userId
def delete_user(id):
    r = requests.delete("http://user-access:5200/v1/users/{}".format(id))
    return r.text

def get_user(id):
    r = requests.get("http://user-access:5200/v1/users/{}".format(id))
    return r.json()

def get_user_id(username):
    r = requests.get("http://user-access:5200/v1/users/getId/{}".format(username))
    return r.text

def patch_user(id):
    r = requests.patch("http://user-access:5200/v1/users/{}".format(id), json=request.json)

