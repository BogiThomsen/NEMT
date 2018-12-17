import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response



user_db = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Users"]
dummy_user = {"_id": "5c157799a8568b000b92e9c4", "accessToken": "b0436d96c40128c9312c05d04eaf4440875876485fd24b4779b235e3",
              "password": "8c1ad979d7d4c40d8f7d6bac7b1d6e7bee01fc79a073d5acf95f77705602485e:06dba173a0ef4970a2523e59fd0cbbf0", "username": "test5", "devices": ["5c15779b438c8700184c3da8", "5c1577a4438c8700184c3dae", "5c1577ad438c8700184c3db4"]}

def post_user():
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
        return make_response(json.dumps(user), 200)


def delete_user(id):
    query = {"_id": ObjectId(id)}
    if (user_db.count_documents(query)) < 1 :
        return make_response(json.dumps({"error": "user with id: "+ id +" does not exists"}), 404)
    else:
        user_db.delete_one(query)
        return make_response("", 200)

def get_user(id):
    if ObjectId.is_valid(id):
        query = {"_id": ObjectId(id)}
    else:
        query = {"accessToken": id}
    #if (user_db.count_documents(query)) < 1 :
        #return make_response(json.dumps({"error": "user with id: "+ id +" does not exist"}), 404)
    #else:
        #x = user_db.find_one(query)
        #x["_id"] = str(x["_id"])
    return make_response(json.dumps(dummy_user), 200)


def get_user_id_by_username(username):
    #query = {"username": username}
    #if (user_db.count_documents(query)) < 1 :
        #return make_response(json.dumps({"error": "user with username: "+ username +" does not exist"}), 404)
    #x = user_db.find_one(query)
    return make_response('5c157799a8568b000b92e9c4', 200)

def patch_user(id):
    lists = {"device", "rule", "grouping", "otherDevices"}
    strings = {"password", "username"}
    ignore_vals = {"_id", "operation"}
    strings_dict = string_dict()
    user = user_db.find_one({"_id": ObjectId(id)})
    for val in request.json:
        if val not in strings and val not in lists and val not in ignore_vals:
            return make_response(val + "is not a patcheable field", 400)
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


