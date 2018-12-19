from flask import jsonify, request, json, make_response
import requests

### Data Access Endpoints

def add_sensor(userid, deviceid):
    """Adds a sensor to the database

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device
        json (json): json object containing an accestoken and the information to create a sensor. 
        

    Returns:
        the sensor as a json object.
    """
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
    """Fetches a list of sensors from the database

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device
        json (json): json object containing an accestoken and an array of ids of the sensors. 
        

    Returns:
        the sensors in an array as a json object.
    """
    sensor_response = requests.get("http://sensor-access:5600/v1/sensors", json=request.json)
    return make_response(sensor_response.content, sensor_response.status_code)

def delete_sensor(userid, deviceid, sensorid):
    """Deletes a sensor from the database

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device
        sensorid (string): the id of the sensor
        json (json): json object containing an accestoken 
        

    Returns:
        200 response if the sensor is deleted, 402 if not.
    """
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
    """Fetches a sensor from the database

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device
        sensorid (string): the id of the sensor
        json (json): json object containing an accestoken
        

    Returns:
        the sensor as a json object.
    """
    sensor_response = requests.get("http://sensor-access:5600/v1/sensors/{}".format(sensorid))
    return make_response(sensor_response.content, sensor_response.status_code)

def patch_sensor(userid, deviceid, sensorid):
    """Updates a sensor

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device
        sensorid (string): the id of the sensor
        json (json): json object containing an accestoken and the information to update a sensor. 
        

    Returns:
        the updated sensor as a json object.
    """
    sensor_response = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response(sensor_response.content, sensor_response.status_code)

def device_patch_sensor(deviceid, sensorid):
    """Updates a sensor value

    Args:
        userid (string): the name of the user
        deviceid (string): the token of the device
        

    Returns:
        200 if the sensor is updated, 402 if not.
    """
    sensor_response = requests.patch("http://sensor-access:5600/v1/sensors/{}".format(sensorid), json=request.json)
    return make_response(sensor_response.content, sensor_response.status_code)
