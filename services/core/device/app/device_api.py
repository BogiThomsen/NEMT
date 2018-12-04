from flask import jsonify, request

devices = []

def addDevice():
    device = {
        'name': request.json['name'],
        'description': request.json['description']
    }
    devices.append(device)
    return jsonify({'device': device}), 201

def getDevice():
    return jsonify(devices)