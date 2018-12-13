from flask import jsonify, request, json
import requests

### Data Access Endpoints

def add_device(userid):
    device = {
        "name" : request.json["name"],
        "device_token" : request.json["device_token"]
    }
    device_response = requests.post("http://device-access:5500/v1/devices", json=device).json()
    created_device = device_response.json()
    json = {
        "operation":"add",
        "device":created_device["device_token"]
    }
    requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=json)
    return make_response(json.dumps(created_device), device_response.status_code)

def delete_device(userid, deviceid):
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()

    for x in device["sensors"]:
        sensordata=x.split(':')
        sensor_id = sensordata[1]
        requests.delete("http://sensor-service:5900/v1/devices/{0}/sensors/{1}".format(deviceid, sensor_id))

    for x in device["actions"]:
        actiondata = x.split(':')
        action_id = actiondata[1]
        requests.delete("http://action-service:5800/v1/devices/{0}/actions/{1}".format(deviceid, action_id))

    json = {
        "operation":"remove",
        "device":deviceid
    }

    device_response = requests.delete("http://device-access:5500/v1/devices/{}".format(deviceid), json=json)

    requests.patch("http://user-service:5100/v1/users/{}".format(userid), json=json)
    return make_response(device_response.content, device_response.status_code)

def get_device(userid, deviceid):
    device_response = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
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
    sensor_response =requests.patch("http://sensor-service:5800/v1/devices/{0}/sensors/{1}".format(deviceid, sensor_id), json=sensor_patch)
    
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
    action_response = requests.patch("http://action-service:5900/v1/devices/{0}/actions/{1}".format(deviceid, action_id), json=action_patch)
    return make_response(action_response.content, action_response.status_code)