from flask import request, make_response
from validator import validate_users_request, validate_devices_request, validate_actions_request, validate_sensors_request
from authorizer import authorize
import requests
import json

core_url = '127.0.0.1:3333/v1'
headers = {'User-Agent': 'web-app-api', 'Content-Type': 'application/json'}

def post_users_authenticate():
    validation = validate_users_request(request)
    if validation == '':
        return requests.post(core_url + '/users/authenticate', headers=headers, data=request.json)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users():
    validation = validate_users_request(request)
    if validation == '':
        return requests.post(core_url + '/users', headers=headers, data=request.json)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_id(id):
    validation = validate_users_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(core_url + '/users/' + id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_id(id):
    validation = validate_users_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(core_url + '/users/' + id, headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_id(id):
    validation = validate_users_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(core_url + '/users/' + id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users_id_devices(id):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.post(core_url + '/users/' + id + '/devices', headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_user_id_devices_device_id(user_id, device_id):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(core_url + '/users/' + user_id + '/devices/' + device_id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_user_id_devices_device_id(user_id, device_id):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(core_url + '/users/' + user_id + '/devices/' + device_id, headers=headers,
                                  data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_user_id_devices_device_id(user_id, device_id):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(core_url + '/users/' + user_id + '/devices/' + device_id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users_id_devices_device_id_actions(user_id, device_id):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.post(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions', headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_id_devices_device_id_actions_action_id(user_id, device_id, action_id):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions/' + action_id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_id_devices_device_id_actions_action_id(user_id, device_id, action_id):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions/' + action_id,
                                  headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_id_devices_device_id_actions_action_id(user_id, device_id, action_id):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions/' + action_id,
                                   headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def post_users_id_devices_device_id_sensors(user_id, device_id):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.post(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors', headers=headers,
                              data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def get_users_id_devices_device_id_sensors_sensor_id(user_id, device_id, sensor_id):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.get(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors/' + sensor_id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def patch_users_id_devices_device_id_sensors_sensor_id(user_id, device_id, sensor_id):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.patch(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors/' + sensor_id,
                                  headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

def delete_users_id_devices_device_id_sensors_sensor_id(user_id, device_id, sensor_id):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json['accessToken'])
        if authorization == '':
            return requests.delete(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors/' + sensor_id,
                                   headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)
