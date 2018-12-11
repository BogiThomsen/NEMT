import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Sensors"]


def Sensor_user():
    sensor_db = connect_to_db()
    name = request.json["name"]
    sensor_db.insert_one({"name": name})
    sensor = sensor_db.find_one({"username": name})
    sensor["_id"] = str(sensor["_id"])
    return sensor


def delete_sensor(id):
    sensor_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor doesnt exist", 400)
    else:
        sensor_db.delete_one(query)
        return "sensor: {}, was deleted.".format(id)

def get_sensor(id):
    sensor_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor doesnt exists", 400)
    else:
        x = sensor_db.find_one(query)
        x["_id"] = str(x["_id"])
        return dumps(x)

def patch_user(id):
    strings = {"password", "username"}
    strings_dict = string_dict()
    lists = {"device", "rule", "grouping", "other_devices"}
    lists_dict = list_dict()
    sensor_db = connect_to_db()
    sensor = sensor_db.find_one({"_id": ObjectId(id)})
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
                if ((val == "username") and (user_db.count_documents({"username": request.json[val]})) > 0):
                    if request.json[val] == user["username"]:
                        continue
                    else:
                        return make_response("username already exists", 400)
                else:
                    user_db.update_one({"_id": ObjectId(id)},
                                       {"$set": {strings_dict[val]: request.json[val]}})


def string_dict():
    dict = {
        "name": "name",
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


