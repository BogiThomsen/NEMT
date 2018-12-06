import pymongo
from bson.objectid import ObjectId

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["datebase"]["Users"]


def post_user(username, password, access_token):
    user_db = connect_to_db()
    new_user = {"username": username, "password": password, "access_token": access_token}
    user_db.insert_one(new_user)


def delete_user(user_id):
    user_db = connect_to_db()
    query = {"_id": ObjectId(user_id)}
    user_db.delete_one(query)


def put_username(user_id, new_username):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                         { "$set": { "username": new_username}})


def put_password(user_id, new_password):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                         { "$set": { "password": new_password}})


def get_user(user_id):
    user_db = connect_to_db()
    x = user_db.find_one({"_id": ObjectId(user_id)})
    x["_id"] = str(x["_id"])
    return x


def get_user_id_by_username(username):
    user_db = connect_to_db()
    x = user_db.find_one({"username": username})
    return str(x["_id"])

def post_to_user(user_id, id_to_add, where_to_add):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                   { "$push":  {where_to_add: id_to_add} })

def delete_from_user(user_id, id_to_remove, Where_to_remove):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                        {"$pull": {Where_to_remove: id_to_remove} })
