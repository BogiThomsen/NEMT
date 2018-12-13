import pymongo
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Sensors"]


def post_sensor():
    sensor_db = connect_to_db()
    name = request.json["name"]
    if 'prettyname' not in request.json:
        new_sensor = {"name": name,
                      "pretty_name": name,
                      "public": False}
    else:
        new_sensor = {"name": name,
                      "pretty_name": request.json["pretty_name"],
                      "public": False}
    _id = sensor_db.insert_one(new_sensor).inserted_id
    sensor = sensor_db.find_one({"_id": _id})
    sensor["_id"] = str(sensor["_id"])
    return make_response(json.dumps(sensor), 201)


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

def patch_sensor(id):
    strings = {"pretty_name", "value", "timestamp", "public"}
    strings_dict = string_dict()
    lists = {"access_token"}
    sensor_db = connect_to_db()
    for val in lists:
        if val in request.json:
            patch_lists(sensor_db, id, request.json, val)
    if request.json["operation"] == "add":
        for val in strings:
            if val in request.json:
                sensor_db.update_one({"_id": ObjectId(id)},
                                       {"$set": {strings_dict[val]: request.json[val]}})
    patched_sensor = sensor_db.find_one({"_id": ObjectId(id)})
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
        "pretty_name": "pretty_name",
        "value": "value",
        "timestamp": "timestamp",
        "public": "public"
    }
    return dict

def list_dict():
    dict = {
        "access_token": "access_tokens"
    }
    return dict


