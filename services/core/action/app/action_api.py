from flask import jsonify, request, json
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
    return created_action

def delete_action(userid, deviceid, actionid):
    action_response = requests.delete("http://action-access:5700/v1/actions/{}".format(actionid))
    json = {
        "operation":"remove",
        "action":actionid
    }
    device_response = requests.patch("http://device-service:5400/v1/users/{0}/devices/{1}".format(userid, deviceid), json=json)
    return action_response.text

def get_action(userid, deviceid, actionid):
    action = requests.get("http://action-access:5700/v1/actions/{}".format(actionid)).json()
    return action

def patch_action(userid, deviceid, actionid):
    r = requests.patch("http://action-access:5700/v1/actions/{}".format(actionid), json=request.json)
    return r.text

def activate_action(userid, deviceid, actionid):
    r = requests.get("http://action-access:5700/v1/actions/{}".format(actionid), json=request.json)
    return r.text
