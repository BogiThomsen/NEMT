import pymongo
from flask import request
from bson.objectid import ObjectId

class UserAccessLayer(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")
        db = client["database"]
        self.user_db = db["Users"]

    def add_user():
    username = request.json['username']
    password = request.json['password']
    access_token = request.json['access_token']

    new_user = {"username": username, "password": password, "access_token": access_token}
    user_db.insert_one(new_user)

    def remove_user(self, user_id):
        query = {"_id": ObjectId(user_id)}
        self.user_db.delete_one(query)

    def change_username(self, user_id, new_username):
        self.user_db.update_one({"_id": ObjectId(user_id)},
                             { "$set": { "username": new_username}})

    def change_password(self, user_id, new_password):
        self.user_db.update_one({"_id": ObjectId(user_id)},
                             { "$set": { "password": new_password}})

    def get_user(self, user_id):
        x = self.user_db.find_one({"_id": ObjectId(user_id)})
        x["_id"] = str(x["_id"])
        return x

    def get_id_by_username(self, username):
        x = self.user_db.find_one({"username": username})
        return str(x["_id"])


    def add_to_user(self, user_id, id_to_add, where_to_add):
        self.user_db.update_one({"_id": ObjectId(user_id)},
                       { "$push":  {where_to_add: id_to_add} })

    def remove_from_user(self, user_id, id_to_remove, Where_to_remove):
        self.user_db.update_one({"_id": ObjectId(user_id)},
                            {"$pull": {Where_to_remove: id_to_remove} })


