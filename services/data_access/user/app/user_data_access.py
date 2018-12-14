import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response



def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Users"]


def post_user():
    user_db = connect_to_db()
    username = request.json["username"]
    if (user_db.count_documents({"username": username})) > 0 :
        return make_response(json.dumps({"error": "user with username: "+ username +" already exists"}), 400)
    else:
        new_user = {
            "username": username,
            "password": request.json["password"],
            "accessToken": request.json["accessToken"]
        }
        user_db.insert_one(new_user)
        user = user_db.find_one({"username": username})
        user["_id"] = str(user["_id"])
        return make_response(json.dumps(user), 201)


def delete_user(id):
    user_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (user_db.count_documents(query)) < 1 :
        return make_response(json.dumps({"error": "user with id: "+ id +" does not exists"}), 404)
    else:
        user_db.delete_one(query)
        return make_response("", 200)

def get_user(id):
    user_db = connect_to_db()
    if ObjectId.is_valid(id):
        query = {"_id": ObjectId(id)}
    else:
        query = {"accessToken": id}
    if (user_db.count_documents(query)) < 1 :
        return make_response(json.dumps({"error": "user with id: "+ id +" does not exist"}), 404)
    else:
        x = user_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)


def get_user_id_by_username(username):
    user_db = connect_to_db()
    x = user_db.find_one({"username": username})
    return make_response(str(x["_id"]), 200)

def patch_user(id):
    lists = {"device", "rule", "grouping", "otherDevices"}
    strings = {"password", "username"}
    ignore_vals = {"_id", "operation"}
    strings_dict = string_dict()
    user_db = connect_to_db()
    user = user_db.find_one({"_id": ObjectId(id)})
    for val in request.json:
        if val in ignore_vals:
            continue
        elif val in lists:
            if 'operation' in request.json:
                patch_lists(user_db, id, request.json, val)
            else:
                make_response("operation field is required for list patching", 400)
        elif val in strings:
            if ((val == "username") and (user_db.count_documents({"username": request.json[val]})) > 0):
                if request.json[val] == user["username"]:
                    continue
                else:
                    return make_response("username: " + request.json[val] + " already exists", 400)
            else:
                user_db.update_one({"_id": ObjectId(id)},
                                   {"$set": {strings_dict[val]: request.json[val]}})
        else:
            return make_response(val + "is not a patcheable field", 400)
    patched_user = user_db.find_one({"_id": ObjectId(id)})
    patched_user["_id"] = str(patched_user["_id"])
    return make_response(json.dumps(patched_user), 200)

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
        "username": "username",
        "password": "password",
    }
    return dict

def list_dict():
    dict = {
        "device": "devices",
        "rule": "rules",
        "grouping": "groupings",
        "otherDevices": "otherDevices"
    }
    return dict


