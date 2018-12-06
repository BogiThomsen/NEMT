import pymongo
from bson.objectid import ObjectId

class DeviceAccessLayer(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")
        db = client["database"]
        self.device_db = db["Devices"]

    def add_device(self, name, mac_address):
        new_device = {"name": name, "mac_address": mac_address}
        self.device_db.insert_one(new_device)

    def remove_device(self, device_id):
        query = {"_id": ObjectId(device_id)}
        self.device_db.delete_one(query)

    def get_device_id_by_name(self, name):
        x = self.device_db.find_one({"name": name})
        return str(x["_id"])

    def change_name(self, device_id, new_name):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                                {"$set": {"name": new_name}})

    def add_to_device(self, device_id, id_to_add, where_to_add):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                       { "$push":  {where_to_add: id_to_add} })

    def remove_from_device(self, device_id, id_to_remove, Where_to_remove):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                            {"$pull": {Where_to_remove: id_to_remove} })


    def update_last_state(self, device_id, sensor_name, value, time):
        self.device_db.update_one({"_id": ObjectId(device_id), "sensor_values.sensor_name": sensor_name},
                                  {"$set":
                                       {
                                           "value": value,
                                       }
                                  }
                                )


    #def tester(self, device_id, sensor_name):
        #print(self.device_db.find_one({"_id": ObjectId(device_id), "sensor_name": [sensor_name]}))
