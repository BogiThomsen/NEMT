from flask import jsonify, request, json, make_response
import requests
from coapthon.client.helperclient import HelperClient
### Data Access Endpoints

def add_action(userid, deviceid):
    sensor = request.json
    action_response = requests.post("http://action-access:5700/v1/actions", json=sensor)
    created_action = action_response.json()
    action_list = []
    action_list.append(created_action["name"]+":"+created_action["_id"])
    device_patch = {
        "operation":"add",
        "action":action_list
    }
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=device_patch)

    return make_response(json.dumps(created_action), action_response.status_code)

def get_actions(userid, deviceid):
    action_response = requests.get("http://action-access:5700/v1/actions", json=request.json)
    return make_response(action_response.content, action_response.status_code)

def delete_action(userid, deviceid, actionid):
    action = requests.get("http://action-access:5700/v1/actions/{}".format(actionid)).json()
    action_list = []
    action_list.append(action["name"]+":"+action["_id"])
    json = {
        "operation":"remove",
        "action":action_list
    }
    action_response = requests.delete("http://action-access:5700/v1/actions/{}".format(actionid))
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=json)
    return make_response(action_response.content, action_response.status_code)

def get_action(userid, deviceid, actionid):
    action_response = requests.get("http://action-access:5700/v1/actions/{}".format(actionid))
    return make_response(json.dumps(action_response.json()), action_response.status_code)

def patch_action(userid, deviceid, actionid):
    patch_response = requests.patch("http://action-access:5700/v1/actions/{}".format(actionid), json=request.json)
    return make_response(patch_response.content, patch_response.status_code)

def activate_action(userid, deviceid, actionid):
    device = requests.get("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid)).json()
    if 'actions' in device:
        for x in device["actions"]:
            actiondata = x.split(':')
            if actionid == actiondata[1]:
                action = actiondata[0]
                break
        token = device["deviceToken"].split(':')
        host = token[0]
        port = int(token[1])
        client = HelperClient(server=(host, port))
        client.put("action", action)
    else:
        make_response("Device has no actions", 400)