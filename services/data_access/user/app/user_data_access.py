import pymongo
from bson.objectid import ObjectId
from flask import Flask, request, make_response

app = Flask(__name__)

def connect_to_db():
    return pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")["datebase"]["Users"]

@app.route('/users', methods=['POST'])
def post_user():
    json = request.args
    user_db = connect_to_db()
    msg = user_db.insert_one(json)
    if msg:
        return make_response('Error', 400)
    else:
        return make_response('Ok', 200)


@app.route('/users/<String:id>', methods=['DELETE'])
def delete_user(id):
    user_db = connect_to_db()
    query = {"_id": ObjectId(id)}
    user_db.delete_one(query)

@app.route('/')
def put_username(user_id, new_username):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                         { "$set": { "username": new_username}})

@app.route('/users/<String:id>', methods=['PUT'])
def put_password(user_id, new_password):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                         { "$set": { "password": new_password}})

@app.route('/')
def get_user(user_id):
    user_db = connect_to_db()
    x = user_db.find_one({"_id": ObjectId(user_id)})
    x["_id"] = str(x["_id"])
    return x

@app.route('/')
def get_user_id_by_username(username):
    user_db = connect_to_db()
    x = user_db.find_one({"username": username})
    return str(x["_id"])

@app.route('/')
def post_to_user(user_id, id_to_add, where_to_add):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                   { "$push":  {where_to_add: id_to_add} })
@app.route('/')
def delete_from_user(user_id, id_to_remove, Where_to_remove):
    user_db = connect_to_db()
    user_db.update_one({"_id": ObjectId(user_id)},
                        {"$pull": {Where_to_remove: id_to_remove} })
