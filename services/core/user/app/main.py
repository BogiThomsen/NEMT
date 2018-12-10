from flask import Flask, request
from services.data_access.user.app import user_data_access
from services.data_access.device import device_data_access
import json
import hashlib
import uuid
import secrets
import connexion

#Setups that is used throughout the user service.
##app = connexion.App(__name__, specification_dir = './')
app = Flask(__name__)
app.add_api('swagger.yml')
data_access = user_data_access.UserAccessLayer()
device_access = device_data_access.DeviceAccessLayer()

@app.route('/user/<String:username>')
def getUser(username):
    user_json = request.get_json(username)
    user_object = json.loads(user_json)
    user_id = data_access.get_user_id_by_username(user_object.username)
    user = json.loads(data_access.get_user(user_id))

    if checkPassword(user.password, user_object.password):
        return
    else:
        return None


@app.route('/user/String:username')
def getUserDevices(username):
    user = getUser(request.json(username))

    #Retrieve list of devices
    #user = x.get_user(x.get_user_id_by_username("default username")) print(user["available_devices"])
    user = json.loads(user)
    user_devices = []

    for device_id in user.available_devices:
        user_devices.append(device_access.get_device(device_id))
    #Return list of devices
    return user_devices


@app.route('/user/String:user')
def patchUsername(user):
    #user = json.loads(data_access.get_user(user_id))
    return None

@app.route('/user/String:user')
def patchUserPassword(user):
    #user = json.loads(data_access.get_user(user_id))
    return None

def hashPassword(password):
    foo = uuid.uuid4().hex
    return hashlib.sha256(foo.encode() + password.encode()).hexdigest() + ':' + foo

def checkPassword(hashedPassword, userPassword):
    password, foo = hashedPassword.split(':')
    return userPassword == hashlib.sha256(foo.encode() + password.encode()).hexdigest()

@app.route('user/String:user')
def postUser(user):
    jsonuser = {
        'username': request.json['username'],
        'password': hashPassword(request.json['password']),
        'access_token': secrets.token_urlsafe(20)
    }

    data_access.post_user(jsonuser)

def deleteUser(user_id):
    return data_access.deleteUser(user_id)



if __name__ == "__main__":
  app.run(debug=True,host='localhost')