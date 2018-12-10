from flask import Flask, request
from services.data_access.user.app import user_data_access
from services.data_access.user.app import device_data_access
import json
import connexion

#Setups that is used throughout the user service.
app = Flask.__name__
data_access = user_data_access.UserAccessLayer()
device_access = device_data_access.DeviceAccessLayer()


@app.route('/user/<String:username>')
def getUser(username):
    user_json = request.get_json(username)
    user_object = json.loads(user_json)
    user_id = data_access.get_user_id_by_username(user_object.username)

    user = json.loads(data_access.get_user(user_id))

    if(user.password != user_object.password):
        return None
    else:
        return user


@app.route('/user/String:user_id')
def getUserDevices(user_id):
    #Unpack json object
    user_id_from_request = request.get_json(user_id)
    #get json object of a user, using get_user from data access layer
    user_json = data_access.get_user(user_id_from_request.user_id)
    #Retrieve list of devices
    #user = x.get_user(x.get_user_id_by_username("default username")) print(user["available_devices"])
    user = json.loads(user_json)
    user_devices = []

    for device_id in user.available_devices:
        user_devices.append(device_access.get_device(device_id))
    #Return list of devices
    return user_devices


@app.route('/user/String:user')
def updateUser(user):
    user = json.loads(data_access.get_user(user))
    data_access.patch(user)

    

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0',  port='5100')