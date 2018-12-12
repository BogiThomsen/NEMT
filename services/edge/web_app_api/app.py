from flask import Flask, request, make_response
from validator import validate_users_request, validate_devices_request, validate_actions_request, validate_sensors_request
from authorizer import authorize
import requests
import json

app = Flask(__name__)

core_url = '127.0.0.1:3333/v1'
headers = {'User-Agent': 'web-app-api', 'Content-Type': 'application/json'}
api_version = 'v1'

@app.route('/' + api_version + '/users/authenticate', methods=['POST'])
def users_authenticate():
    validation = validate_users_request(request)
    if validation == '':
        return requests.post(core_url + '/users/authenticate', headers=headers, data=request.json)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users', methods=['POST'])
def users():
    validation = validate_users_request(request)
    if validation == '':
        return requests.post(core_url + '/users', headers=headers, data=request.json)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users/<string:id>', methods=['GET', 'PATCH', 'DELETE'])
def users_id(id):
    if request.method == 'PATCH':
        validation = validate_users_request(request)
    else:
        validation = ''

    if validation == '':
        authorization = authorize(request.json.accessToken)
        if authorization == '':
            if request.method == 'GET':
                return requests.get(core_url + '/users/' + id, headers=headers)
            elif request.method == 'PATCH':
                return requests.patch(core_url + '/users/' + id, headers=headers, data=request.json.data)
            else:
                return requests.delete(core_url + '/users/' + id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users/<string:id>/devices', methods=['POST'])
def users_id_devices(id):
    validation = validate_devices_request(request)
    if validation == '':
        authorization = authorize(request.json.accessToken)
        if authorization == '':
            return requests.post(core_url + '/users/' + id + '/devices', headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users/<string:user_id>/devices/<string:device_id>', methods=['GET', 'PATCH', 'DELETE'])
def users_user_id_devices_device_id(user_id, device_id):
    if request.method == 'PATCH':
        validation = validate_devices_request(request)
    else:
        validation = True

    if validation == '':
        authorization = authorize(request.json.accessToken)
        if authorization == '':
            if request.method == 'GET':
                return requests.get(core_url + '/users/' + user_id + '/devices/' + device_id, headers=headers)
            elif request.method == 'PATCH':
                return requests.patch(core_url + '/users/' + user_id + '/devices/' + device_id, headers=headers, data=request.json.data)
            else:
                return requests.delete(core_url + '/users/' + user_id + '/devices/' + device_id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users/<string:user_id>/devices/<string:device_id>/actions', methods=['POST'])
def users_id_devices_device_id_actions(user_id, device_id):
    validation = validate_actions_request(request)
    if validation == '':
        authorization = authorize(request.json.accessToken)
        if authorization == '':
            return requests.post(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions', headers=headers, data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users/<string:user_id>/devices/<string:device_id>/actions/<string:action_id>', methods=['GET', 'PATCH', 'DELETE'])
def users_id_devices_device_id_actions_action_id(user_id, device_id, action_id):
    if request.method == 'PATCH':
        validation = validate_actions_request(request)
    else:
        validation = True

    if validation == '':
        authorization = authorize(request.json.accessToken)
        if authorization == '':
            if request.method == 'GET':
                return requests.get(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions/' + action_id, headers=headers)
            elif request.method == 'PATCH':
                return requests.patch(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions/' + action_id, headers=headers, data=request.json.data)
            else:
                return requests.delete(core_url + '/users/' + user_id + '/devices/' + device_id + '/actions/' + action_id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users/<string:user_id>/devices/<string:device_id>/sensors', methods=['POST'])
def users_id_devices_device_id_sensors(user_id, device_id):
    validation = validate_sensors_request(request)
    if validation == '':
        authorization = authorize(request.json.accessToken)
        if authorization == '':
            return requests.post(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors', headers=headers,
                              data=request.json.data)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

@app.route('/' + api_version + '/users/<string:user_id>/devices/<string:device_id>/sensors/<string:sensor_id>', methods=['GET', 'PATCH', 'DELETE'])
def users_id_devices_device_id_sensors_sensor_id(user_id, device_id, sensor_id):
    if request.method == 'PATCH':
        validation = validate_sensors_request(request)
    else:
        validation = True

    if validation == '':
        authorization = authorize(request.json.accessToken)
        if authorization == '':
            if request.method == 'GET':
                return requests.get(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors/' + sensor_id, headers=headers)
            elif request.method == 'PATCH':
                return requests.patch(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors/' + sensor_id, headers=headers, data=request.json.data)
            else:
                return requests.delete(core_url + '/users/' + user_id + '/devices/' + device_id + '/sensors/' + sensor_id, headers=headers)
        else:
            return make_response(json.dumps({"error": authorization, "body": request.json}), 401, headers)
    else:
        return make_response(json.dumps({"error": validation, "body": request.json}), 400, headers)

if __name__ == "__main__":
  app.run(debug=True)
