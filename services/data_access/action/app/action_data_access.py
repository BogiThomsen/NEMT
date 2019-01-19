import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response

#Sets up the mongoClient containing connection pools for the action database
action_db =  pymongo.MongoClient('localhost', 27017)["database"]["Actions"]


def post_action():
    """adds an action to the database,
        if a prettyName is included it is used,
        otherwise the name becomes the prettyName.

        Body:
            Args:
                name (string): Name of the action
                public (bool): Whether or not the device is public
                prettyName (string): can potentially be included for the user to set its own name for the action


        Returns:
            the action.

        """
    name = request.json["name"]
    if 'prettyName' not in request.json:
        new_action = {"name": name,
                      "prettyName": name,
                      "public": request.json["public"]}
    else:
        new_action = {"name": name,
                      "prettyName": request.json["prettyName"],
                      "public": request.json["public"]}
    _id = action_db.insert_one(new_action).inserted_id
    action = action_db.find_one({"_id": _id})
    action["_id"] = str(action["_id"])
    return make_response(json.dumps(action), 200)


def delete_action(id):
    """deletes an action from the database given an action_id

        path:
            Args:
                _id (string): id of the action

        Returns:
            empty string with a status code of 200.

        """
    query = {"_id": ObjectId(id)}
    if (action_db.count_documents(query)) < 1 :
        return make_response("action with id: " + id + " doesnt exist", 404)
    else:
        action_db.delete_one(query)
        return make_response("", 200)


def get_action(id):
    """Gets an action from the database

        path:
            Args:
                _id (string): id of the action

        Returns:
            all information on an action from the database given an action_id

        """
    query = {"_id": ObjectId(id)}
    if (action_db.count_documents(query)) < 1 :
        return make_response("action with id: " + id + " doesnt exist", 404)
    else:
        x = action_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)

def get_actions():
    """Gets all actions from the database in a given actionList,
    used when presenting all actions a device has in the user interface.

        Body:
            Args:
                actionList (array of strings): list of action ids

        Returns:
            all information regarding all actions in the given actionList

        """
    action_list = request.json["actionList"]
    ids = [ObjectId(id) for id in action_list]
    liste = list(action_db.find({"_id": {"$in": ids}}))
    actions = []
    for action in liste:
        action["_id"] = str(action["_id"])
        actions.append(action)


    return make_response(json.dumps(actions), 200)


#,
#
def patch_action(id):
    """patches action information,
    changes prettyName and public status when the proper id is given
    if the accessToken list should be updated, one must also include an operation value of either 'add' or 'remove'

        path:
            Args:
                id (string): id of the action
        Body:
            Args:
                json object containing information to be patched

        Returns:
            all information regarding the patched action

        """
    strings = {"prettyName", "public"}
    strings_dict = string_dict()
    lists = {"accessToken"}
    ignore_vals = {"_id", "operation"}
    lists_dict = list_dict()
    for val in request.json:
        if val not in strings and val not in lists and val not in ignore_vals:
            return make_response(val + "is not a patcheable field", 400)
    for val in request.json:
        if val in ignore_vals:
            continue
        elif val in lists:
            if 'operation' in request.json:
                if request.json["operation"] == "remove":
                    for item in request.json[val]:
                        action_db.update_one({"_id": ObjectId(id)},
                                           {"$pull": {lists_dict[val]: item}})
                if request.json["operation"] == "add":
                    for item in request.json[val]:
                        action_db.update_one({"_id": ObjectId(id)},
                                           {"$addToSet": {lists_dict[val]: item}})
            else:
                make_response("operation field is required for list patching", 400)
        elif val in strings:
                action_db.update_one({"_id": ObjectId(id)},
                                       {"$set": {strings_dict[val]: request.json[val]}})
        else:
            return make_response(val + "is not a patcheable field", 400)
    patched_action = action_db.find_one({"_id": ObjectId(id)})
    patched_action["_id"] = str(patched_action["_id"])
    return make_response(json.dumps(patched_action), 200)


#dictionaries used for the patch function, Could be made redundant or moved to some sort of configuration file.
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


