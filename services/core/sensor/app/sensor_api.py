from flask import jsonify, request, json
import requests

### Data Access Endpoints

def add_sensor(userid, devicetoken):
    sensor = {
        "name" : request.json["name"],
        "token" : request.json["token"]
    }
    created_sensor = requests.post("http://sensor-access:5600/v1/sensors", json=sensor).json()
    json = {
        "operation":"add",
        "sensor":created_sensor["name"]+":"+created_sensor["_id"]
    }
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, devicetoken), json=json)
    return created_sensor

def delete_sensor(userid, devicetoken, sensorid):
    sensor_response = requests.delete("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    json = {
        "operation":"remove",
        "sensor":sensorid
    }
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, devicetoken), json=json)
    return sensor_response.text

def get_sensor(userid, devicetoken, sensorid):
    sensor = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid)).json()
    return sensor

def patch_sensor(userid, devicetoken, sensorid):
    r = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return r.text
