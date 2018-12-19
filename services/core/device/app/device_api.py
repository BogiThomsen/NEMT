from flask import jsonify, request, make_response
import json
import requests
import sys

### Data Access Endpoints

def add_device(userid):
    """Adds a device to the database

    Args:
        userid (string): the id of the user
        json (json): json object containing an accestoken and the information to create a device. 
        

    Returns:
        the device as a json object.

    """
    device = request.json
    
    device_response = requests.post("http://device-access:5500/v1/devices", json=device)
    
    if device_response.status_code == 200:
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

def get_devices(userid):
    """Fetches a list of devices from the database, based on ids.

    Args:
        json (json): json object containing an accestoken and an array of ids of the Devices

    Returns:
        the Devices.

    """
    device_response = requests.get("http://device-access:5500/v1/devices", json=request.json)
    return make_response(device_response.content, device_response.status_code)

def delete_device(userid, deviceid):
    """deletes a device from the database, based on an id. 
        Also deletes all the actions and sensors linked to that device, 
        and removes the device from the users deviceList.

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device 
        json (json): json object containing an accestoken

        

    Returns:
        200 if the device was deleted, 400 if not.

    """
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
    """Fetches a device from the database, based on an id.

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device 
        json (json): json object containing an accestoken
        

    Returns:
        the device as a json object.

    """
    device_response = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid))
    return make_response(device_response.content, device_response.status_code)

def patch_device(userid, deviceid):
    """updates a device information.

    Args:
        userid (string): the id of the user
        deviceid (string): the id of the device 
        json (json): json object containing an accestoken and the information to be updated on the device.
        

    Returns:
        the device as a json object.

    """
    device_response = requests.patch("http://device-access:5500/v1/devices/{}".format(deviceid), json=request.json)
    return make_response(device_response.content, device_response.status_code)

def patch_sensor_values(deviceid, sensorid):
    """Request and update of a sensor, based on device token and sensor name.

    Args:
        deviceid (string): the token of the device
        sensorid (string): the name of the sensor 
        

    Returns:
        200 if sensor is updated, 402 if not.

    """
    device = requests.get("http://device-access:5500/v1/devices/{}".format(deviceid)).json()
    sensor_patch = request.json

    #Iterate thorugh the list of sensors and match sensorid
    if 'sensors' in device:
        for x in device["sensors"]:
            sensordata=x.split(':')
            if sensordata[0] == sensorid:
                sensor_id = sensordata[1]
                requests.patch("http://sensor-service:5900/v1/devices/{0}/sensors/{1}".format(deviceid, sensor_id), json=sensor_patch)
                return make_response("sensor updated", 200)    
        return make_response(json.dumps({"error:":"sensor not found"}), 402)
    else:
        return make_response(json.dumps({"error:":"sensor not found"}), 402)
    
    
    #When sensor is found, make get request for sensor
    #When sensor is retrieved, update sensor with body and make patch request
