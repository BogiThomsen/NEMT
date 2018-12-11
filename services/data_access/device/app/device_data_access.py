import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Devices"]

def post_device():
    device_db = connect_to_db()
    new_device = {
        "name": request.json["name"],
        "pretty_name": request.json["name"],
        "token": request.json["token"]
    }
    _id = device_db.insert_one(new_device)
    device = device_db.find_one({"_id": _id})
    device["_id"] = str(device["_id"])
    return device

def delete_device(id):
    device_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (device_db.count_documents(query)) < 1 :
        return make_response("device doesnt exist", 400)
    else:
        device_db.delete_one(query)
        return "device: {}, was deleted.".format(id)

def get_device(id):
    device_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (device_db.count_documents(query)) < 1 :
        return make_response("device doesnt exists", 400)
    else:
        x = device_db.find_one(query)
        x["_id"] = str(x["_id"])
        return dumps(x)


def patch_device(id):
    strings = {"pretty_name"}
    strings_dict = string_dict()
    lists = {"sensor", "rule", "action"}
    lists_dict = list_dict()
    device_db = connect_to_db()
    for val in lists:
        if val in request.json:
            if request.json["operation"]:
                for item in request.json[val]:
                    user_db.update_one({"_id": ObjectId(id)},
                                       {"$pull": {lists_dict[val]: item}})
            if request.json["operation"] == False:
                for item in request.json[val]:
                    user_db.update_one({"_id": ObjectId(id)},
                                       {"$addToSet": {lists_dict[val]: item}})
    if request.json["operation"] == False:
        for val in strings:
            if val in request.json:
                user_db.update_one({"_id": ObjectId(id)},
                                    {"$set": {strings_dict[val]: request.json[val]}})

def string_dict():
    dict = {
        "pretty_name": "pretty_name"
    }
    return dict

def list_dict():
    dict = {
        "action": "actions",
        "rule": "rules",
        "sensor": "sensors"
    }
    return dict


