from flask import jsonify, request, json, make_response
import requests

### Data Access Endpoints

def add_sensor(userid, devicetoken):
    sensor = {
        "name" : request.json["name"]
    }
    sensor_response = requests.post("http://sensor-access:5600/v1/sensors", json=sensor)
    created_sensor = sensor_response.json()
    json = {
        "operation":"add",
        "sensor":created_sensor["name"]+":"+created_sensor["_id"]
    }
    requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, devicetoken), json=json)
    return make_response(sensor_response.content, sensor_response.status_code)

def delete_sensor(userid, devicetoken, sensorid):
    sensor_response = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    sensor = sensor_response.json()
    json = {
        "operation":"remove",
        "sensor":sensor["name"]+":"+sensor["_id"]
    }
    sensor_response = requests.delete("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, devicetoken), json=json)
    return make_response(sensor_response.content, sensor_response.status_code)

def get_sensor(userid, devicetoken, sensorid):
    sensor_response = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    return make_response(sensor_response.content, sensor_response.status_code)

def patch_sensor(userid, devicetoken, sensorid):
    response = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response(response.content, response.status_code)

def device_patch_sensor(devicetoken, sensorid):
    response = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response(response.content, response.status_code)
