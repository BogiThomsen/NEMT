import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Actions"]


def post_action():
    action_db = connect_to_db()
    name = request.json["name"]
    if 'prettyName' not in request.json:
        new_action = {"name": name,
                      "prettyName": name,
                      "public": False}
    else:
        new_action = {"name": name,
                      "prettyName": request.json["prettyName"],
                      "public": False}
    _id = action_db.insert_one(new_action).inserted_id
    action = action_db.find_one({"_id": _id})
    action["_id"] = str(action["_id"])
    return make_response(json.dumps(action), 201)


def delete_action(id):
    action_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (action_db.count_documents(query)) < 1 :
        return make_response("action with id: " + id + " doesnt exist", 404)
    else:
        action_db.delete_one(query)
        return make_response("", 200)

def get_action(id):
    action_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (action_db.count_documents(query)) < 1 :
        return make_response("action with id: " + id + " doesnt exist", 404)
    else:
        x = action_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)

def patch_action(id):
    strings = {"prettyName", "public"}
    strings_dict = string_dict()
    lists = {"accessToken"}
    lists_dict = list_dict()
    action_db = connect_to_db()
    for val in lists:
        if val in request.json:
            if request.json["operation"] == "remove":
                for item in request.json[val]:
                    action_db.update_one({"_id": ObjectId(id)},
                                       {"$pull": {lists_dict[val]: item}})
            if request.json["operation"] == "add":
                for item in request.json[val]:
                    action_db.update_one({"_id": ObjectId(id)},
                                       {"$addToSet": {lists_dict[val]: item}})
    if request.json["operation"] == "add":
        for val in strings:
            if val in request.json:
                action_db.update_one({"_id": ObjectId(id)},
                                       {"$set": {strings_dict[val]: request.json[val]}})


def string_dict():
    dict = {
        "prettyName": "prettyName",
        "public": "public"
    }
    return dict

def list_dict():
    dict = {
        "accessToken": "accessTokens"
    }
    return dict


