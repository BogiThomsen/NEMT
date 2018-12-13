from flask import jsonify, request, json, make_response
import requests

### Data Access Endpoints

def add_sensor(userid, devicetoken):
    sensor = {
        "name" : request.json["name"]
    }
    created_sensor = requests.post("http://sensor-access:5600/v1/sensors", json=sensor).json()
    json = {
        "operation":"add",
        "sensor":created_sensor["name"]+":"+created_sensor["_id"]
    }
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, devicetoken), json=json)
    return make_response(json.dumps(created_sensor), 200)

def delete_sensor(userid, devicetoken, sensorid):
    sensor = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid)).json()
    json = {
        "operation":"remove",
        "sensor":sensor["name"]+":"+sensor["_id"]
    }
    sensor_response = requests.delete("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, devicetoken), json=json)
    return make_response("??????????", 200)

def get_sensor(userid, devicetoken, sensorid):
    sensor = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid)).json()
    return make_response(json.dumps(sensor), 200)

def patch_sensor(userid, devicetoken, sensorid):
    r = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response("??????????", 200)

def device_patch_sensor(devicetoken, sensorid):
    r = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response("??????????", 200)
