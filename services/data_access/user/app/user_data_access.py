import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://Andreas:dummypassword64@sw7-3mptj.gcp.mongodb.net/admin")
db = client["database"]

user_db = db["Users"]

def add_user(username, password, access_token):
    new_user = {"username": username, "password": password, "access_token": access_token}
    user_db.insert_one(new_user)

def remove_user(user_id):
    query = {"_id": ObjectId(user_id)}
    user_db.delete_one(query)

def change_username(user_id, new_username):
    user_db.update_one({"_id": ObjectId(user_id)},
                         { "$set": { "username": new_username}})

def change_password(user_id, new_password):
    user_db.update_one({"_id": ObjectId(user_id)},
                         { "$set": { "password": new_password}})

def get_user(user_id):
    x = user_db.find_one({"_id": ObjectId(user_id)})
    x["_id"] = str(x["_id"])
    return x

def get_id_by_username(username):
    x = user_db.find_one({"username": username})
    return str(x["_id"])


#def add_device_to_user(user_id)




#Testies
#add_user("LarsAllan", "1234567", "Second_Breakfast47")

##remember to find id
#id_to_remove = "dummyid"
#remove_user(id_to_remove)

id_to_change_name = "5c067e0f6025271da8e45fab"
#change_username(id_to_change_name, "Changed Username")

#change_password(id_to_change_name, "newPassword")
print(get_user(id_to_change_name))
print(get_user("5c0678f36025271d7857066b"))

print(get_id_by_username("LarsAllan"))