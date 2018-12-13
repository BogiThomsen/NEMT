import pymongo
import re
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Devices"]

def post_device():
    device_db = connect_to_db()
    url = "http://192.168.99.100:5500/v1/devices"
    mac_address = request.json["device_token"]
    if (device_db.count_documents({"device_token": mac_address})) > 0 :
        return make_response(json.dumps({"error": "device with Mac Address: "+ mac_address + "already exists"}), 400)
    if 'pretty_name' not in request.json:
        pretty_name = request.json["name"]
    else:
        pretty_name = request.json['pretty_name']
    new_device = {
        "name": request.json["name"],
        "pretty_name": pretty_name,
        "device_token": request.json["device_token"]
    }
    _id = device_db.insert_one(new_device).inserted_id
    device = device_db.find_one({"_id": _id})
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
        query = {"device_token": id}
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
    strings = {"pretty_name"}
    strings_dict = string_dict()
    lists = {"sensor", "rule", "action"}
    device_db = connect_to_db()
    for val in lists:
        if val in request.json:
            patch_lists(device_db, id, request.json, val)
    if request.json["operation"] == "add":
        for val in strings:
            if val in request.json:
                device_db.update_one({"_id": ObjectId(id)},
                                    {"$set": {strings_dict[val]: request.json[val]}})
    patched_device = device_db.find_one({"_id": ObjectId(id)})
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
        "pretty_name": "pretty_name",
    }
    return dict

def list_dict():
    dict = {
        "action": "actions",
        "rule": "rules",
        "sensor": "sensors"
    }
    return dict


