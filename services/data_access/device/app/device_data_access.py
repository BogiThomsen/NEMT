import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Devices"]


def post_device():
    device_db = connect_to_db()
    devicename = request.json["devicename"]

    if (device_db.count_documents({"devicename": devicename})) > 0 :
        return make_response("devicename exists", 400)
    else:
        new_device = {
            "devicename": devicename,
            "password": request.json["password"],
            "access_token": request.json["access_token"]
        }
        device_db.insert_one(new_device)
        return "device: {}, was added".format(devicename)


def delete_device(id):
    device_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (device_db.count_documents(query)) < 1 :
        return make_response("device doesnt exist", 400)
    else:
        device_db.delete_one(query)
        return "device: {}, was deleted.".format(id)

def patch_devicename():
    devicename = request.json["devicename"]
    device_id = request.json["deviceId"]
    device_db = connect_to_db()
    if (device_db.count_documents({"devicename": devicename})) > 0 :
        return make_response("devicename exists", 400)
    else:
        device_db.update_one({"_id": ObjectId(device_id)},
                            { "$set": { "devicename": devicename}})

def patch_password():
    new_password = request.json["password"]
    device_id = request.json["deviceId"]
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                         { "$set": { "password": new_password}})

def get_device(id):
    device_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (device_db.count_documents(query)) < 1 :
        return make_response("device doesnt exists", 400)
    else:
        x = device_db.find_one(query)
        x["_id"] = str(x["_id"])
        return dumps(x)


def get_device_id_by_devicename(devicename):
    device_db = connect_to_db()
    x = device_db.find_one({"devicename": devicename})
    return str(x["_id"])

def add_to_device():
    device_id = request.json["deviceId"]
    id_to_add = request.json["updateId"]
    where_to_add = request.json["updateList"]
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                   { "$addToSet":  {where_to_add: id_to_add} })

def delete_from_device():
    device_id = request.json["deviceId"]
    id_to_remove = request.json["updateId"]
    where_to_remove = request.json["updateList"]
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                        {"$pull": {where_to_remove: id_to_remove} })


def patch_device(id):
    strings = {"name"}
    strings_dict = string_dict()
    lists = {"sensor", "rule", "action"}
    lists_dict = list_dict()
    device_db = connect_to_db()
    for val in lists:
        if val in request.json:
            if request.json["operation"]:
                device_db.update_one({"_id": ObjectId(id)},
                                   {"$pull": {lists_dict[val]: request.json[val]}})
            if request.json["operation"] == False:
                device_db.update_one({"_id": ObjectId(id)},
                                   {"$addToSet": {lists_dict[val]: request.json[val]}})
    for val in strings:
        if val in request.json:
            if ((val == "name") and (device_db.count_documents({"name": request.json[val]})) > 0):
                return make_response("name already exists", 400)
            else:
                device_db.update_one({"_id": ObjectId(id)},
                                   {"$set": {strings_dict[val]: request.json[val]}})


def string_dict():
    dict = {
        "name": "name"
    }
    return dict

def list_dict():
    dict = {
        "action": "actions",
        "rule": "rules",
        "sensor": "sensors"
    }
    return dict


