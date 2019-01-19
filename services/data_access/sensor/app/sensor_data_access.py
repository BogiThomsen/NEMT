import pymongo
import json
from bson.objectid import ObjectId
from flask import request, make_response

#Sets up the mongoClient containing connection pools for the sensor database
sensor_db = pymongo.MongoClient('localhost', 27017)["database"]["Sensors"]


def post_sensor():
    """adds a sensor to the database,
        if a prettyName is included it is used,
        otherwise the name becomes the prettyName.

        Body:
            Args:
                name (string): Name of the sensor
                public (bool): Whether or not the device is public
                prettyName (string): can potentially be included for the user to set its own name for the action


        Returns:
            the sensor

        """
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
    """deletes a sensor from the database given an sensor_id

        path:
            Args:
                _id (string): id of the sensor

        Returns:
            empty string with a status code of 200.

        """
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor with id: " + id + " doesnt exist", 404)
    else:
        sensor_db.delete_one(query)
        return make_response("", 200)

def get_sensor(id):
    """Gets an sensor from the database

        path:
            Args:
                _id (string): id of the action

        Returns:
            all information on an sensor from the database given an sensor_id

        """
    query = {"_id": ObjectId(id)}
    if (sensor_db.count_documents(query)) < 1 :
        return make_response("sensor with id: " + id + " doesnt exist", 404)
    else:
        x = sensor_db.find_one(query)
        x["_id"] = str(x["_id"])
        return make_response(json.dumps(x), 200)

def get_sensors():
    """Gets all sensors from the database in a given sensorList,
    used when presenting all sensors a device has in the user interface.

        Body:
            Args:
                sensorList (array of strings): list of sensor ids

        Returns:
            all information regarding all sensors in the given sensorList

        """
    sensor_list = request.json["sensorList"]
    ids = [ObjectId(id) for id in sensor_list]
    liste = list(sensor_db.find({"_id": {"$in": ids}}))
    sensors = []
    for sensor in liste:
        sensor["_id"] = str(sensor["_id"])
        sensors.append(sensor)


    return make_response(json.dumps(sensors), 200)

def patch_sensor(id):
    """patches sensor information,
    changes prettyName, value, timestamp and the public boolean if the proper id is given
    if the accessToken list should be updated, one must also include an operation value of either 'add' or 'remove'
    patching lists makes use of the patch_lists helper function.
        path:
            Args:
                id (string): id of the device
        Body:
            Args:
                json object containing information to be patched

        Returns:
            all information regarding the patched sensor

        """
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
            sensor_db.update_one({"_id": ObjectId(id)},
                                   {"$set": {strings_dict[val]: request.json[val]}})
        else:
            return make_response(val + "is not a patcheable field", 400)
    patched_sensor = sensor_db.find_one({"_id": ObjectId(id)})
    patched_sensor["_id"] = str(patched_sensor["_id"])
    return make_response(json.dumps(patched_sensor), 200)

def patch_lists(db, id, json_object, current_val):
    """patches sensor information if the information is stored in a list,
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


