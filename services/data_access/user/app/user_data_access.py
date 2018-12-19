import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response


#Sets up the mongoClient containing connection pools for the user database
user_db = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Users"]


def post_user():
    """adds a user to the database,
        Body:
            Args:
                name (string): Name of the action
                accessToken (string): The access token generated for the user
                password (string): hashed password

        Returns:
            the user.

        """
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
    """deletes a user from the database given an user_id

        path:
            Args:
                _id (string): id of the user

        Returns:
            empty string with a status code of 200.

        """
    query = {"_id": ObjectId(id)}
    if (user_db.count_documents(query)) < 1 :
        return make_response(json.dumps({"error": "user with id: "+ id +" does not exists"}), 404)
    else:
        user_db.delete_one(query)
        return make_response("", 200)

def get_user(id):
    """Gets a user from the database

        path:
            Args:
                _id (string): id of the user or the access token

        Returns:
            all information on an user from the database given an action_id

        """
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
    """Gets a user id from the database

        path:
            Args:
                username (string): username of the user

        Returns:
            user id

        """
    query = {"username": username}
    if (user_db.count_documents(query)) < 1 :
        return make_response(json.dumps({"error": "user with username: "+ username +" does not exist"}), 404)
    x = user_db.find_one(query)
    return make_response(str(x["_id"]), 200)

def patch_user(id):
    """patches user information,
    changes password and username when the proper id is given
    if the device, rule, grouping or otherDevices list should be updated, one must also include an operation value of either 'add' or 'remove'
    uses patch_lists as a helper function to patch values in lists
        path:
            Args:
                id (string): id of the user
        Body:
            Args:
                json object containing information to be patched

        Returns:
            all information regarding the patched action

        """
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
    """patches user information if the information is stored in a list,
        helper function for the patch_user method
        path:
            Args:
                db (MongoClient): the MongoClient used for connection pooling
                id (string): id of the device
                json_object (object): json object containing the information to be patched.
                current_val (string): current value in the json object

        Returns:
            nothing

        """
    lists_dict = list_dict()
    if json_object["operation"] == "remove":
        for item in json_object[current_val]:
            db.update_one({"_id": ObjectId(id)},
                               {"$pull": {lists_dict[current_val]: item}})
    if json_object["operation"] == "add":
        for item in json_object[current_val]:
            db.update_one({"_id": ObjectId(id)},
                               {"$addToSet": {lists_dict[current_val]: item}})

#dictionaries used for the patch function, Could be made redundant or moved to some sort of configuration file.
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


