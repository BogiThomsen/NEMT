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
    sensor_patch = request.json()

    #Iterate thorugh the list of sensors and match sensorid
    for x in device["sensors"]:
        sensordata=x.split(':')
        if sensordata[0] == sensorname:
            sensor_id = sensordata[1]
            break
    requests.patch("http://sensor-service:5800/v1/devices/{0}/sensors/{1}".format(deviceid, sensor_id), json=sensor_patch)

    #When sensor is found, make get request for sensor
    #When sensor is retrieved, update sensor with body and make patch request

def patch_action_values(deviceid, actionname):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    action_patch = request.json()

    #Iterate thorugh the list of actions and match actionid
    for x in device["actions"]:
        actiondata=x.split(':')
        if actiondata[0] == actionname:
            action_id = actiondata[1]
            break
    requests.patch("http://action-service:5900/v1/devices/{0}/actions/{1}".format(deviceid, action_id), json=action_patch)
