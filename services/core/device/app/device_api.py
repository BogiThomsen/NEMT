from flask import jsonify, request, json
import requests

### Data Access Endpoints

def add_device(userid):
    device = {
        "name" : request.json["name"],
        "token" : request.json["token"]
    }
    created_device = requests.post("http://device-access:5500/v1/devices", json=device).json()
    json = {
        "operation":"add",
        "device":created_device["_id"]
    }
    user_response = requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=json)
    return created_device

def delete_device(userid, deviceid):
    device_response = requests.delete("http://device-access:5500/v1/devices/{}".format(deviceid))
    json = {
        "operation":"remove",
        "device":deviceid
    }
    user_response = requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=json)
    return device_response.text

def get_device(userid, deviceid):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    return device

def patch_device(userid, deviceid):
    r = requests.patch("http://device-access:5500/v1/devices/{}".format(deviceid), json=request.json)
    return r.text
