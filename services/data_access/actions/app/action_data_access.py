import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Actions"]


def post_action():
    action_db = connect_to_db()
    name = request.json["name"]
    if 'prettyname' not in request.json:
        new_action = {"name": name,
                      "pretty_name": name,
                      "public": False}
    else:
        new_action = {"name": name,
                      "pretty_name": request.json["pretty_name"],
                      "public": False}
    _id = action_db.insert_one(new_action).inserted_id
    action = action_db.find_one({"_id": _id})
    action["_id"] = str(action["_id"])
    return action


def delete_action(id):
    action_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (action_db.count_documents(query)) < 1 :
        return make_response("action doesnt exist", 400)
    else:
        action_db.delete_one(query)
        return "action: {}, was deleted.".format(id)

def get_action(id):
    action_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (action_db.count_documents(query)) < 1 :
        return make_response("action doesnt exists", 400)
    else:
        x = action_db.find_one(query)
        x["_id"] = str(x["_id"])
        return dumps(x)

def patch_action(id):
    strings = {"name", "pretty_name", "public"}
    strings_dict = string_dict()
    lists = {"access_token"}
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
        "name": "name",
        "pretty_name": "pretty_name",
        "public": "public"
    }
    return dict

def list_dict():
    dict = {
        "access_token": "access_tokens"
    }
    return dict


