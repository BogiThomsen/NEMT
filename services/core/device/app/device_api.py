from flask import jsonify, request, json
import requests

### Data Access Endpoints

def add_device(userid):
    device = {
        "name" : request.json["name"],
        "device_token" : request.json["device_token"]
    }
    created_device = requests.post("http://device-access:5500/v1/devices", json=device).json()
    json = {
        "operation":"add",
        "device":created_device["device_token"]
    }

    requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=json)
    return created_device

def delete_device(userid, deviceid):
    device_response = requests.delete("http://device-access:5500/v1/devices/{}".format(deviceid))
    json = {
        "operation":"remove",
        "device":deviceid
    }
    requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=json)
    return device_response.text

def get_device(userid, deviceid):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    return device

def patch_device(userid, deviceid):
    r = requests.patch("http://device-access:5500/v1/devices/{}".format(deviceid), json=request.json)
    return r.text

def patch_sensor_values(deviceid, sensorname):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    updates_to_sensor = request.json["sensor"]
    sensorid = None
    device["sensors"]

    #Iterate thorugh the list of sensors and match sensorid
    for x[1] in device["sensors"]:
        if x == sensorname:
            sensorid = x[2]
            break

    sensor = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid)).json()
    sensor["value"] = updates_to_sensor["value"]
    requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensor["id"]), json=sensor)

    #When sensor is found, make get request for sensor
    #When sensor is retrieved, update sensor with body and make patch request
