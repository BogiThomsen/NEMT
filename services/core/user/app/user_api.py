from flask import jsonify, request
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
    r = requests.post("http://user-access:5200/api/add", json=user)
    return jsonify({'response': r})

def delete_user():
    user = get_user_id(request.json["userId"])
    r = requests.post("http://user-access:5200/api/delete", json=user)
    return jsonify({'response': r})

def get_user():

    user = get_user_id(request.json["userId"])
    r = requests.get("http://user-access:5200/api/get", json=user)
    return jsonify({'user' : r.json})

def get_user_id():
    user = {
        "username" : : request.json["username"]
    }
    r = requests.get("http://user-access:5200/api/getId"
    return jsonify('userId' : r.json))


def update_username():
    user = {
        "userId" : requests.json["userId"],
        "username" : requests,json["username"]
    }
    r = requests.patch("http://user-access:5200/api/update/username", json=user)
    return jsonify('response' : r)

def update_password():
    user = {
        "userId" : requests.json["userId"],
        "password" : requests,json["password"]
    }
    r = requests.patch("http://user-access:5200/api/update/password", json=user)
    return jsonify('response' : r)

def add_device_to_user():
    update = {
        "userId" : requests.json["userId"],
        "updateId" : request.json["deviceId"]
        "updateList" : "available_devices"
    }
    r = requests.patch("http://user-access:5200/api/list/add", json=user)
    return jsonify({'response' : r})

def remove_device_from_user():
    update = {
        "userId" : requests.json["userId"],
        "updateId" : request.json["deviceId"]
        "updateList" : "available_devices"
    }
    r = requests.patch("http://user-access:5200/api/list/remove", json=user)
    return jsonify({'response' : r})

def add_rule_to_user():
    update = {
        "userId" : requests.json["userId"],
        "updateId" : request.json["ruleId"]
        "updateList" : "rules"
    }
    r = requests.patch("http://user-access:5200/api/list/add", json=user)
    return jsonify({'response' : r})

def remove_rule_from_user():
    update = {
        "userId" : requests.json["userId"],
        "updateId" : request.json["ruleId"]
        "updateList" : "rules"
    }
    r = requests.patch("http://user-access:5200/api/list/remove", json=user)
    return jsonify({'response' : r})

def add_group_to_user():
    update = {
        "userId" : requests.json["userId"],
        "updateId" : request.json["groupId"]
        "updateList" : "groupings"
    }
    r = requests.patch("http://user-access:5200/api/list/add", json=user)
    return jsonify({'response' : r})

def remove_group_from_user():
    update = {
        "userId" : requests.json["userId"],
        "updateId" : request.json["groupId"]
        "updateList" : "groupings"
    }
    r = requests.patch("http://user-access:5200/api/list/remove", json=user)
    return jsonify({'response' : r})