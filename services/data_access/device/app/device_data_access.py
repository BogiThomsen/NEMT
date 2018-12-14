import pymongo
import re
import json
from bson.objectid import ObjectId
from flask import request, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Devices"]

def post_device():
    device_db = connect_to_db()
    mac_address = request.json["deviceToken"]
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
    return make_response(json.dumps(device), 201)

def delete_device(id):
    device_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (device_db.count_documents(query)) < 1 :
        return make_response("device with id: "+ id +" doesnt exist", 404)
    else:
        device_db.delete_one(query)
        return make_response("", 200)

def get_device(id):
    device_db = connect_to_db()
    r = re.compile('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    if ObjectId.is_valid(id):
        query = {"_id": ObjectId(id)}
        type = "id"
    elif r.match(id).group() == id:
        query = {"deviceToken": id}
        type = "token"
    else:
        return make_response(json.dumps({"error": "value: " + id + " is not a valid id or token"}), 400)
    if (device_db.count_documents(query)) < 1 :
        return make_response(json.dumps({"error": "device with" + type + ": " + id +" does not exists"}), 404)
    else:
        x = device_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)


def patch_device(id):
    strings = {"prettyName"}
    strings_dict = string_dict()
    lists = {"sensor", "rule", "action"}
    ignore_vals = {"_id", "operation"}
    device_db = connect_to_db()
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


