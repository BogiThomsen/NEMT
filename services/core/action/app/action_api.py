from flask import jsonify, request, json, make_response
import requests

### Data Access Endpoints

def add_action(userid, deviceid):
    action = {
        "name" : request.json["name"]
    }
    created_action = requests.post("http://action-access:5700/v1/actions", json=action).json()
    json = {
        "operation":"add",
        "action":created_action["name"]+":"+created_action["_id"]
    }
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=json)
    action = created_action.json()

    return make_response(json.dumps(action), created_action.status_code)

def delete_action(userid, deviceid, actionid):
    action = requests.get("http://action-access:5700/v1/actions/{}".format(actionid)).json()
    json = {
        "operation":"remove",
        "action":action["name"]+":"+action["_id"]
    }
    action_response = requests.delete("http://action-access:5700/v1/actions/{}".format(actionid))
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=json)
    return make_response(json.dumps(action_response.json()), action_response.status_code)

def get_action(userid, deviceid, actionid):
    action_response = requests.get("http://action-access:5700/v1/actions/{}".format(actionid))
    return make_response(json.dumps(action_response.json()), action_response.status_code)

def patch_action(userid, deviceid, actionid):
    patch_response = requests.patch("http://action-access:5700/v1/actions/{}".format(actionid), json=request.json)
    return make_response(json.dumps(patch_response.json()), patch_response.status_code)

def activate_action(userid, deviceid, actionid):
    device = requests.get("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid)).json()

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