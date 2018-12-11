from flask import jsonify, request, json
import requests

### Data Access Endpoints

def add_device():
    device = {
        "devicename" : request.json["devicename"]
    }
    r = requests.post("http://device-access:5200/v1/devices", json=device)
    return jsonify({'response': r.json()})

def delete_device(id):
    r = requests.delete("http://device-access:5200/v1/devices/{}".format(id))
    return r.text

def get_device(id):
    r = requests.get("http://device-access:5200/v1/devices/{}".format(id))
    return r.json()

# def get_device_id(devicename):
#     r = requests.get("http://device-access:5200/v1/devices/getId/{}".format(devicename))
#     return r.text

def patch_device(id):
    r = requests.patch("http://device-access:5200/v1/devices/{}".format(id), json=request.json)

