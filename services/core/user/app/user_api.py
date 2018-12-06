from flask import jsonify, request
import requests

users = []

def addUser():
    user = {
        "username" : request.json["username"],
        "password" : request.json["password"],
        "access_token" : request.json["access_token"]
    }
    r = requests.post("http://172.20.0.3:5300/api/addUser", json=user)
    return jsonify({'request': r.status_code})

def getUser():
    return jsonify(users)