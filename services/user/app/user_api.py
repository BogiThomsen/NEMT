from flask import jsonify, request

users = []

def addUser():
    user = {
        'username': request.json['username'],
        'email': request.json['email']
    }
    users.append(user)
    return jsonify({'user': user}), 201

def getUser():
    return users