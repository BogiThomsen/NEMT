import pymongo
import re
import json
from bson.objectid import ObjectId
from flask import request, make_response

device_db = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Devices"]
dummy_device = {"_id": "5c1577ad438c8700184c3db4", "name": "device003", "prettyName": "Coffee Machine", "deviceToken": "170.34.94.158:5687",
                "actions": ["action005:5c1577aee3dcad000bdc8cc2", "action006:5c1577b0e3dcad000bdc8cc4"],
                "sensors": ["sensor005:5c1577b117d37c000b6a9f7b"]}
def post_device():
    r = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{4}$')
    mac_address = request.json["deviceToken"]
    if r.match(mac_address).group() != mac_address:
        return make_response(json.dumps({"error": mac_address + " is not a valid device token"}), 400)
    if (device_db.count_documents({"deviceToken": mac_address})) > 0 :
        return make_response(json.dumps({"error": "device with Mac Address: "+ mac_address + " already exists"}), 400)
    if 'prettyName' not in request.json:
        pretty_name = request.json["name"]
    else:
        pretty_name = request.json['prettyName']
    new_device = {
        "name": request.json["name"],
        "prettyName": pretty_name,
        "deviceToken": request.json["deviceToken"]
    }
    _id = device_db.insert_one(new_device).inserted_id
    device = device_db.find_one({"deviceToken": request.json["deviceToken"]})
    device["_id"] = str(device["_id"])
    return make_response(json.dumps(device), 200)

def delete_device(id):
    query = {"_id": ObjectId(id)}
    if (device_db.count_documents(query)) < 1 :
        return make_response("device with id: "+ id +" doesnt exist", 404)
    else:
        device_db.delete_one(query)
        return make_response("", 200)

def get_device(id):
    r = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{4}$')
    if ObjectId.is_valid(id):
        query = {"_id": ObjectId(id)}
        type = "id"
    elif r.match(id).group() == id:
        query = {"deviceToken": id}
        type = "token"
    else:
        return make_response(json.dumps({"error": "value: " + id + " is not a valid id or token"}), 400)
    #if (device_db.count_documents(query)) < 1 :
        #return make_response(json.dumps({"error": "device with" + type + ": " + id +" does not exists"}), 404)
    #x = device_db.find_one(query)
    #x["_id"] = str(x["_id"])
    return make_response(json.dumps(dummy_device), 200)

def get_devices():
    device_list = request.json["deviceList"]
    ids = [ObjectId(id) for id in device_list]
    #liste = list(device_db.find({"_id": {"$in": ids}}))
    devices = []
    #for device in liste:
    #    device["_id"] = str(device["_id"])
    #    devices.append(device)


    return make_response(json.dumps([dummy_device]), 200)


def patch_device(id):
    strings = {"prettyName"}
    strings_dict = string_dict()
    lists = {"sensor", "rule", "action"}
    ignore_vals = {"_id", "operation"}
    for val in request.json:
        if val not in strings and val not in lists and val not in ignore_vals:
            return make_response(val + "is not a patcheable field", 400)
    for val in request.json:
        if val in ignore_vals:
            continue
        elif val in lists:
            if 'operation' in request.json:
                patch_lists(device_db, id, request.json, val)
            else:
                make_response("operation field is required for list patching", 400)
        elif val in strings:
            device_db.update_one({"_id": ObjectId(id)},
                                {"$set": {strings_dict[val]: request.json[val]}})
        else:
            return make_response(val + "is not a patcheable field", 400)
    patched_device = device_db.find_one({"_id": ObjectId(id)})
    patched_device["_id"] = str(patched_device["_id"])
    return make_response(json.dumps(patched_device), 200)

def patch_lists(db, id, json_object, current_val):
    lists_dict = list_dict()
    if json_object["operation"] == "remove":
        for item in json_object[current_val]:
            db.update_one({"_id": ObjectId(id)},
                               {"$pull": {lists_dict[current_val]: item}})
    if json_object["operation"] == "add":
        for item in json_object[current_val]:
            db.update_one({"_id": ObjectId(id)},
                               {"$addToSet": {lists_dict[current_val]: item}})
def string_dict():
    dict = {
        "prettyName": "prettyName",
    }
    return dict

def list_dict():
    dict = {
        "action": "actions",
        "rule": "rules",
        "sensor": "sensors"
    }
    return dict


