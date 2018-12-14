from flask import jsonify, request, make_response
import json
import requests

### Data Access Endpoints

def add_device(userid):
    device = {
        "name" : request.json["name"],
        "deviceToken" : request.json["deviceToken"]
    }
    
    if 'prettyName' in request.json:
        device["prettyName"] = request.json["prettyName"]

    device_response = requests.post("http://device-access:5500/v1/devices", json=device)
    
    if device_response.status_code == 201:
        created_device = device_response.json()
        device_list = []
        device_list.append(created_device["_id"])
        patch_device = {
            "operation":"add",
            "device":device_list
        }
        user_response = requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=patch_device)
        return make_response(device_response.content, device_response.status_code)
    else:
        return make_response(device_response.content, device_response.status_code)

def delete_device(userid, deviceid):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    if 'sensors' in device:
        for x in device["sensors"]:
            sensordata=x.split(':')
            sensor_id = sensordata[1]
            requests.delete("http://sensor-service:5900/v1/users/{0}/devices/{1}/sensors/{2}".format(userid, deviceid, sensor_id))
    if 'actions' in device:
        for x in device["actions"]:
            actiondata = x.split(':')
            action_id = actiondata[1]
            requests.delete("http://action-service:5800/v1/users/{0}/devices/{1}/actions/{2}".format(userid, deviceid, action_id))

    device_list = []
    device_list.append(deviceid)
    patch_device = {
        "operation":"remove",
        "device":device_list
    }

    device_response = requests.delete("http://device-access:5500/v1/devices/{}".format(deviceid))

    requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=patch_device)
    return make_response(device_response.content, device_response.status_code)

def get_device(userid, deviceid):
    device_response = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid))
    return make_response(device_response.content, device_response.status_code)

def patch_device(userid, deviceid):
    device_response = requests.patch("http://device-access:5500/v1/devices/{}".format(deviceid), json=request.json)
    return make_response(device_response.content, device_response.status_code)

def patch_sensor_values(deviceid, sensorid):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    sensor_patch = request.json()

    #Iterate thorugh the list of sensors and match sensorid
    for x in device["sensors"]:
        sensordata=x.split(':')
        if sensordata[0] == sensorid:
            sensor_id = sensordata[1]
            break
    sensor_response = requests.patch("http://sensor-service:5900/v1/devices/{0}/sensors/{1}".format(deviceid, sensor_id), json=sensor_patch)
    
    return make_response(sensor_response.content, sensor_response.status_code)
    #When sensor is found, make get request for sensor
    #When sensor is retrieved, update sensor with body and make patch request

def patch_action_values(deviceid, actionid):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    action_patch = request.json()

    #Iterate thorugh the list of actions and match actionid
    for x in device["actions"]:
        actiondata=x.split(':')
        if actiondata[0] == actionid:
            action_id = actiondata[1]
            break
    action_response = requests.patch("http://action-service:5800/v1/devices/{0}/actions/{1}".format(deviceid, action_id), json=action_patch)
    return make_response(action_response.content, action_response.status_code)