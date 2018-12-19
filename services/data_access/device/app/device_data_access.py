import pymongo
import re
import json
from bson.objectid import ObjectId
from flask import request, make_response

#Sets up the mongoClient containing connection pools for the device database
device_db = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["database"]["Devices"]

def post_device():
    """adds a device to the database,
        if a prettyName is included it is used,
        otherwise the name becomes the prettyName.

        Body:
            Args:
                name (string): Name of the action
                deviceToken (string): The Mac address of the device
                prettyName (string): can potentially be included for the user to set its own name for the action


        Returns:
            the device.

        """
    r = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{4}$')
    mac_address = request.json["deviceToken"]
    if r.match(mac_address).group() != mac_address:
        return make_response(json.dumps({"error": mac_address + " is not a valid device token"}), 400)
    if (device_db.count_documents({"deviceToken": mac_address})) > 0 :
        return make_response(json.dumps({"error": "device with Mac Address: "+ mac_address + " already exists"}), 400)
    if 'prettyName' not in request.json:
        pretty_name = request.json["name"]
    else:
        pretty_name = request.json['prettyName']
    new_device = {
        "name": request.json["name"],
        "prettyName": pretty_name,
        "deviceToken": request.json["deviceToken"]
    }
    _id = device_db.insert_one(new_device).inserted_id
    device = device_db.find_one({"deviceToken": request.json["deviceToken"]})
    device["_id"] = str(device["_id"])
    return make_response(json.dumps(device), 200)

def delete_device(id):
    """deletes a device from the database given an device_id

        path:
            Args:
                id (string): id of the device

        Returns:
            empty string with a status code of 200.

        """
    query = {"_id": ObjectId(id)}
    if (device_db.count_documents(query)) < 1 :
        return make_response("device with id: "+ id +" doesnt exist", 404)
    else:
        device_db.delete_one(query)
        return make_response("", 200)

def get_device(id):
    """Gets a device from the database
    can take both a device_id or a device mac_address

        path:
            Args:
                id (string): id of the device or the deviceToken of the device

        Returns:
            all information on a device from the database

        """
    r = re.compile('^(?:[0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{4}$')
    if ObjectId.is_valid(id):
        query = {"_id": ObjectId(id)}
        type = "id"
    elif r.match(id).group() == id:
        query = {"deviceToken": id}
        type = "token"
    else:
        return make_response(json.dumps({"error": "value: " + id + " is not a valid id or token"}), 400)
    if (device_db.count_documents(query)) < 1 :
        return make_response(json.dumps({"error": "device with" + type + ": " + id +" does not exists"}), 404)
    else:
        x = device_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)

def get_devices():
    """Gets all devices from the database in a given deviceList,
    used when presenting all devices a yser has in the user interface.

        Body:
            Args:
                deviceList (array of strings): list of device ids

        Returns:
            all information regarding all devices in the given actionList

        """
    device_list = request.json["deviceList"]
    ids = [ObjectId(id) for id in device_list]
    liste = list(device_db.find({"_id": {"$in": ids}}))
    devices = []
    for device in liste:
        device["_id"] = str(device["_id"])
        devices.append(device)


    return make_response(json.dumps(devices), 200)



def patch_device(id):
    """patches device information,
    changes prettyName the proper id is given
    if the sensors,rule or actions list should be updated, one must also include an operation value of either 'add' or 'remove'
    patching lists makes use of the patch_lists helper function.
        path:
            Args:
                id (string): id of the device
        Body:
            Args:
                json object containing information to be patched

        Returns:
            all information regarding the patched device

        """
    strings = {"prettyName"}
    strings_dict = string_dict()
    lists = {"sensor", "rule", "action"}
    ignore_vals = {"_id", "operation"}
    for val in request.json:
        if val not in strings and val not in lists and val not in ignore_vals:
            return make_response(val + "is not a patcheable field", 400)
    for val in request.json:
        if val in ignore_vals:
            continue
        elif val in lists:
            if 'operation' in request.json:
                patch_lists(device_db, id, request.json, val)
            else:
                make_response("operation field is required for list patching", 400)
        elif val in strings:
            device_db.update_one({"_id": ObjectId(id)},
                                {"$set": {strings_dict[val]: request.json[val]}})
        else:
            return make_response(val + "is not a patcheable field", 400)
    patched_device = device_db.find_one({"_id": ObjectId(id)})
    patched_device["_id"] = str(patched_device["_id"])
    return make_response(json.dumps(patched_device), 200)


def patch_lists(db, id, json_object, current_val):
    """patches device information if the information is stored in a list,
        helper function for the patch_device method
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
        "prettyName": "prettyName",
    }
    return dict

def list_dict():
    dict = {
        "action": "actions",
        "rule": "rules",
        "sensor": "sensors"
    }
    return dict


