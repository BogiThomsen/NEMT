import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Sensors"]


def post_sensor():
    sensor_db = connect_to_db()
    name = request.json["name"]
    if 'prettyName' not in request.json:
        new_sensor = {"name": name,
                      "prettyName": name,
                      "public": request.json["public"]}
    else:
        new_sensor = {"name": name,
                      "prettyName": request.json["prettyName"],
                      "public": request.json["public"]}
    _id = sensor_db.insert_one(new_sensor).inserted_id
    sensor = sensor_db.find_one({"_id": _id})
    sensor["_id"] = str(sensor["_id"])
    return make_response(json.dumps(sensor), 200)


def delete_sensor(id):
    sensor_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor with id: " + id + " doesnt exist", 404)
    else:
        sensor_db.delete_one(query)
        return make_response("", 200)

def get_sensor(id):
    sensor_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor with id: " + id + " doesnt exist", 404)
    else:
        x = sensor_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)

def get_sensors():
    sensor_db = connect_to_db()
    sensor_list = request.json["sensorList"]
    ids = [ObjectId(id) for id in sensor_list]
    liste = list(sensor_db.find({"_id": {"$in": ids}}))
    sensors = []
    for sensor in liste:
        sensor["_id"] = str(sensor["_id"])
        sensors.append(sensor)


    return make_response(json.dumps(sensors), 200)

def patch_sensor(id):
    strings = {"prettyName", "value", "timestamp", "public"}
    ignore_vals = {"_id", "operation"}
    strings_dict = string_dict()
    lists = {"accessToken"}
    sensor_db = connect_to_db()
    for val in request.json:
        if val not in strings and val not in lists and val not in ignore_vals:
            return make_response(val + "is not a patcheable field", 400)
    for val in request.json:
        if val in ignore_vals:
            continue
        elif val in lists:
            if 'operation' in request.json:
                patch_lists(sensor_db, id, request.json, val)
            else:
                make_response("operation field is required for list patching", 400)
        elif val in strings:
            sensor_db.update_one({"_id": ObjectId(id)},
                                   {"$set": {strings_dict[val]: request.json[val]}})
        else:
            return make_response(val + "is not a patcheable field", 400)
    patched_sensor = sensor_db.find_one({"_id": ObjectId(id)})
    patched_sensor["_id"] = str(patched_sensor["_id"])
    return make_response(json.dumps(patched_sensor), 200)

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
        "value": "value",
        "timestamp": "timestamp",
        "public": "public"
    }
    return dict

def list_dict():
    dict = {
        "accessToken": "accessTokens"
    }
    return dict


