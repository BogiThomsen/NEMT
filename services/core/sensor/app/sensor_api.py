from flask import jsonify, request, json, make_response
import requests

### Data Access Endpoints

def add_sensor(userid, deviceid):
    sensor = request.json
    sensor_response = requests.post("http://sensor-access:5600/v1/sensors", json=sensor)
    created_sensor = sensor_response.json()
    sensor_list = []
    sensor_list.append(created_sensor["name"]+":"+created_sensor["_id"])
    patch_sensor = {
        "operation":"add",
        "sensor":sensor_list
    }
    requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=patch_sensor)
    return make_response(sensor_response.content, sensor_response.status_code)

def get_sensors(userid, deviceid):
    sensor_response = requests.get("http://sensor-access:5600/v1/sensors", json=request.json)
    return make_response(sensor_response.content, sensor_response.status_code)

def delete_sensor(userid, deviceid, sensorid):
    sensor_response = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    sensor = sensor_response.json()
    sensor_list = []
    sensor_list.append(sensor["name"]+":"+sensor["_id"])
    patch_sensor = {
        "operation":"remove",
        "sensor":sensor_list
    }
    sensor_response = requests.delete("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=patch_sensor)
    return make_response(sensor_response.content, sensor_response.status_code)

def get_sensor(userid, deviceid, sensorid):
    sensor_response = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    return make_response(sensor_response.content, sensor_response.status_code)

def patch_sensor(userid, deviceid, sensorid):
    sensor_response = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response(sensor_response.content, sensor_response.status_code)

def device_patch_sensor(deviceid, sensorid):
    sensor_response = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response(sensor_response.content, sensor_response.status_code)
