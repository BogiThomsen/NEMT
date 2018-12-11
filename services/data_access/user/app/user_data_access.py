import pymongo
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify, make_response

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Users"]


def post_user():
    user_db = connect_to_db()
    username = request.json["username"]

    if (user_db.count_documents({"username": username})) > 0 :
        return make_response("username exists", 400)
    else:
        new_user = {
            "username": username,
            "password": request.json["password"],
            "access_token": request.json["access_token"]
        }
        user_db.insert_one(new_user)
        return "user: {}, was added".format(username)


def delete_user(id):
    user_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (user_db.count_documents(query)) < 1 :
        return make_response("user doesnt exist", 400)
    else:
        user_db.delete_one(query)
        return "user: {}, was deleted.".format(id)

def patch_username():
    username = request.json["username"]
    user_id = request.json["userId"]
    user_db = connect_to_db()
    if (user_db.count_documents({"username": username})) > 0 :
        return make_response("username exists", 400)
    else:
        user_db.update_one({"_id": ObjectId(user_id)},
                            { "$set": { "username": username}})

def patch_password():
    new_password = request.json["password"]
    user_id = request.json["userId"]
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                         { "$set": { "password": new_password}})

def get_user(id):
    user_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    if (user_db.count_documents(query)) < 1 :
        return make_response("user doesnt exists", 400)
    else:
        x = user_db.find_one(query)
        x["_id"] = str(x["_id"])
        return dumps(x)


def get_user_id_by_username(username):
    user_db = connect_to_db()
    x = user_db.find_one({"username": username})
    return str(x["_id"])

def add_to_user():
    user_id = request.json["userId"]
    id_to_add = request.json["updateId"]
    where_to_add = request.json["updateList"]
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                   { "$addToSet":  {where_to_add: id_to_add} })

def delete_from_user():
    user_id = request.json["userId"]
    id_to_remove = request.json["updateId"]
    where_to_remove = request.json["updateList"]
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                        {"$pull": {where_to_remove: id_to_remove} })


def patch_user(id):
    strings = {"password", "username"}
    strings_dict = string_dict()
    lists = {"device", "rule", "grouping", "other_devices"}
    lists_dict = list_dict()
    user_db = connect_to_db()
    for val in lists:
        if val in request.json:
            if request.json["operation"]:
                user_db.update_one({"_id": ObjectId(id)},
                                   {"$pull": {lists_dict[val]: request.json[val]}})
            if request.json["operation"] == False:
                user_db.update_one({"_id": ObjectId(id)},
                                   {"$addToSet": {lists_dict[val]: request.json[val]}})
    for val in strings:
        if val in request.json:
            if ((val == "username") and (user_db.count_documents({"username": request.json[val]})) > 0):
                return make_response("username already exists", 400)
            else:
                user_db.update_one({"_id": ObjectId(id)},
                                   {"$set": {strings_dict[val]: request.json[val]}})


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
        "other_device": "other_devices"
    }
    return dict

