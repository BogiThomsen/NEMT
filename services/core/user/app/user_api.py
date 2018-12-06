from flask import jsonify, request
import requests

users = []
user1 = {
    "username" : "testuser",
    "password" : "testpass",
    "access_token" : "cooltoken"
}
users.append(user1)

def addUser():
    user = {
        "username" : request.json["username"],
        "password" : request.json["password"],
        "access_token" : request.json["access_token"]
    }
    r = requests.post("http://user-access:5200/api/addUser", json=user)
    return jsonify({'request': r.status_code})

def getUser():
    return jsonify(users)