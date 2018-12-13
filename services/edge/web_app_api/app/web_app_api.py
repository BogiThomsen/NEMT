from flask import request, make_response
from validator import validate_users_request, validate_devices_request, validate_actions_request, validate_sensors_request
from authorizer import authorize
import requests
import json

user_url = 'http://user-service:5100/v1'
device_url = 'http://device-service:5200/v1'
action_url = 'http://action-service:5800/v1'
sensor_url = 'http://sensor-service:5900/v1'

headers = {'User-Agent': 'web-app-api', 'Content-Type': 'application/json'}

def post_users_authenticate():
    validation = validate_users_request(request)
    if validation == '':
        return requests.post(user_url + '/users/authenticate', headers=headers, data=request.json)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users():
    validation = validate_users_request(request)
    if validation == '':
        return requests.post(user_url + '/users', headers=headers, data=request.json)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_id(id):
    validation = validate_users_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(user_url + '/users/' + id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_id(id):
    validation = validate_users_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(user_url + '/users/' + id, headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_id(id):
    validation = validate_users_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(user_url + '/users/' + id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users_id_devices(id):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.post(device_url + '/users/' + id + '/devices', headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_user_id_devices_device_id(userid, deviceid):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(device_url + '/users/' + userid + '/devices/' + deviceid, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_user_id_devices_device_id(userid, deviceid):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(device_url + '/users/' + userid + '/devices/' + deviceid, headers=headers,
                                  data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_user_id_devices_device_id(userid, deviceid):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(device_url + '/users/' + userid + '/devices/' + deviceid, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users_user_id_devices_device_id_actions(userid, deviceid):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.post(action_url + '/users/' + userid + '/devices/' + deviceid + '/actions', headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_user_id_devices_device_id_actions_action_id(userid, deviceid, actionid):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(action_url + '/users/' + userid + '/devices/' + deviceid + '/actions/' + actionid, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_user_id_devices_device_id_actions_action_id(userid, deviceid, actionid):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(action_url + '/users/' + userid + '/devices/' + deviceid + '/actions/' + actionid,
                                  headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_user_id_devices_device_id_actions_action_id(userid, deviceid, actionid):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(action_url + '/users/' + userid + '/devices/' + deviceid + '/actions/' + actionid,
                                   headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users_user_id_devices_device_id_sensors(userid, deviceid):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.post(sensor_url + '/users/' + userid + '/devices/' + deviceid + '/sensors', headers=headers,
                              data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_user_id_devices_device_id_sensors_sensor_id(userid, deviceid, sensorid):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(sensor_url + '/users/' + userid + '/devices/' + deviceid + '/sensors/' + sensorid, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_user_id_devices_device_id_sensors_sensor_id(userid, deviceid, sensorid):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(sensor_url + '/users/' + userid + '/devices/' + deviceid + '/sensors/' + sensorid,
                                  headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_user_id_devices_device_id_sensors_sensor_id(userid, deviceid, sensorid):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(sensor_url + '/users/' + userid + '/devices/' + deviceid + '/sensors/' + sensorid,
                                   headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)
