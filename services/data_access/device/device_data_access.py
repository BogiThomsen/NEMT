import pymongo
from bson.objectid import ObjectId

class DeviceAccessLayer(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")
        db = client["database"]
        self.device_db = db["Devices"]

    def post_device(self, device):
        self.device_db.insert_one(device)

    def delete_device(self, device_id):
        query = {"_id": ObjectId(device_id)}
        self.device_db.delete_one(query)

    def get_device_id_by_name(self, name):
        x = self.device_db.find_one({"name": name})
        return str(x["_id"])

    def get_device(self, device_id):
        x = self.device_db.find_one({"_id": ObjectId(device_id)})
        x["_id"] = str(x["_id"])
        return x

    def put_name(self, device_id, new_name):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                                {"$set": {"name": new_name}})

    def post_sensor(self, device_id, sensor):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                       { "$push":  {"sensors": sensor} })

    def delete_sensor(self, device_id, sensor_id):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                            {"$pull": {"sensors": { "id": sensor_id}}})

    def post_action(self, device_id, action):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                       { "$push":  {"actions": action} })

    def delete_action(self, device_id, action_id):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                            {"$pull": {"actions": { "id": action_id}}})

    def put_last_state(self, device_id, sensor_id, value, time):
        self.device_db.update_one({"_id": ObjectId(device_id), "last_state.sensor_values.sensor_id": sensor_id},
                                  {"$set":
                                       {
                                           "last_state.sensor_values.$.value": value,
                                           "last_state.sensor_values.$.timestamp": time
                                       }
                                  }
                                )
    def post_rule(self, device_id, rule_id):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                       { "$push":  {"rules": rule_id} })

    def delete_rule(self, device_id, rule_id):
        self.device_db.update_one({"_id": ObjectId(device_id)},
                       { "$pull":  {"rules": rule_id} })

    def post_sensor_access_token(self, device_id, sensor_id, access_token):
        self.device_db.update_one({"_id": ObjectId(device_id), "sensors.id": sensor_id},
                                  {"$push": {"sensors.$.access_tokens": access_token}})

    def delete_sensor_access_token(self, device_id, sensor_id, access_token):
        self.device_db.update_one({"_id": ObjectId(device_id), "sensors.id": sensor_id},
                                  {"$pull": {"sensors.$.access_tokens": access_token}})

    #def tester(self, device_id, sensor_name):
        #print(self.device_db.find_one({"_id": ObjectId(device_id), "sensor_name": [sensor_name]}))
