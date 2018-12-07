import pymongo
from bson.objectid import ObjectId


def connect_to_db():
    db = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")
    return db["database"]["Devices"]

def post_device(device):
    device_db = connect_to_db()
    device_db.insert_one(device)

def delete_device(device_id):
    device_db = connect_to_db()
    query = {"_id": ObjectId(device_id)}
    device_db.delete_one(query)

def get_device_id_by_name(name):
    device_db = connect_to_db()
    x = device_db.find_one({"name": name})
    return str(x["_id"])

def get_device(device_id):
    device_db = connect_to_db()
    x = device_db.find_one({"_id": ObjectId(device_id)})
    x["_id"] = str(x["_id"])
    return x

def get_devices(device_id_list):
    device_db = connect_to_db()
    object_id_list = [ObjectId(id) for id in device_id_list]
    x = device_db.find({
        "_id": {"$in": object_id_list}
    })
    return x

def put_name(device_id, new_name):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                            {"$set": {"name": new_name}})

def post_sensor(device_id, sensor):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                   { "$push":  {"sensors": sensor} })

def delete_sensor(device_id, sensor_id):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                        {"$pull": {"sensors": { "id": sensor_id}}})

def post_action(device_id, action):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                   { "$push":  {"actions": action} })

def delete_action(device_id, action_id):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                        {"$pull": {"actions": { "id": action_id}}})

def put_last_state(device_id, sensor_id, value, time):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id), "last_state.sensor_values.sensor_id": sensor_id},
                              {"$set":
                                   {
                                       "last_state.sensor_values.$.value": value,
                                       "last_state.sensor_values.$.timestamp": time
                                   }
                              }
                            )
def post_rule(device_id, rule_id):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                   { "$push":  {"rules": rule_id} })

def delete_rule(device_id, rule_id):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id)},
                   { "$pull":  {"rules": rule_id} })

def post_sensor_access_token(device_id, sensor_id, access_token):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id), "sensors.id": sensor_id},
                              {"$push": {"sensors.$.access_tokens": access_token}})

def delete_sensor_access_token(device_id, sensor_id, access_token):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id), "sensors.id": sensor_id},
                              {"$pull": {"sensors.$.access_tokens": access_token}})

def post_action_access_token(device_id, action_id, access_token):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id), "sensors.id": action_id},
                              {"$push": {"actions.$.access_tokens": access_token}})

def delete_action_access_token(device_id, action_id, access_token):
    device_db = connect_to_db()
    device_db.update_one({"_id": ObjectId(device_id), "sensors.id": action_id},
                              {"$pull": {"actions.$.access_tokens": access_token}})


#def tester(self, device_id, sensor_name):
    #print(self.device_db.find_one({"_id": ObjectId(device_id), "sensor_name": [sensor_name]}))


