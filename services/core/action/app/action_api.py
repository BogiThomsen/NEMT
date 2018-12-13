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
    return make_response(json.dumps(created_action), 200)

def delete_action(userid, deviceid, actionid):
    action = requests.get("http://action-access:5700/v1/actions/{}".format(actionid)).json()
    json = {
        "operation":"remove",
        "action":action["name"]+":"+action["_id"]
    }
    action_response = requests.delete("http://action-access:5700/v1/actions/{}".format(actionid))
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=json)
    return make_response("?????????", 200)

def get_action(userid, deviceid, actionid):
    action = requests.get("http://action-access:5700/v1/actions/{}".format(actionid)).json()
    return make_response(json.dumps(action), 200)

def patch_action(userid, deviceid, actionid):
    r = requests.patch("http://action-access:5700/v1/actions/{}".format(actionid), json=request.json)
    return make_response("?????????", 200)

def activate_action(userid, deviceid, actionid):
    r = requests.get("http://action-access:5700/v1/actions/{}".format(actionid), json=request.json)
    return make_response("?????????????", 200)
