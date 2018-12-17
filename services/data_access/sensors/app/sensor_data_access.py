import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response

sensor_db = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Sensors"]
dummy_sensor = [{"_id": "5c1577b117d37c000b6a9f7b", "name": "sensor005", "prettyName": "Coffee Temperature", "public": False, "value": "3", "timestamp": "11-12@09:11"}]

def post_sensor():
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
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor with id: " + id + " doesnt exist", 404)
    else:
        sensor_db.delete_one(query)
        return make_response("", 200)

def get_sensor(id):
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor with id: " + id + " doesnt exist", 404)
    else:
        x = sensor_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)

def get_sensors():
    sensor_list = request.json["sensorList"]
    ids = [ObjectId(id) for id in sensor_list]
    #liste = list(sensor_db.find({"_id": {"$in": ids}}))
    #sensors = []
    #for sensor in liste:
        #sensor["_id"] = str(sensor["_id"])
        #sensors.append(dummy_sensor)


    return make_response(json.dumps(dummy_sensor), 200)

def patch_sensor(id):
    strings = {"prettyName", "value", "timestamp", "public"}
    ignore_vals = {"_id", "operation"}
    strings_dict = string_dict()
    lists = {"accessToken"}
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
            return make_response("", 200)
        else:
            return make_response(val + "is not a patcheable field", 400)
    patched_sensor = sensor_db.find_one({"_id": ObjectId(id)})
    patched_sensor["_id"] = str(patched_sensor["_id"])
    return make_response("", 200)

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


