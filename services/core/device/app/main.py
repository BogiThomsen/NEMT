from flask import Flask, render_template, request
import connexion
import services.data_access.device.device_data_access as data_access

app = connexion.App(__name__, specification_dir = './')
app.add_api('swagger.yml')


#@app.route('/')
#def index():
#    return render_template('index.html', devices=devices)

@app.route('/devices/String:device_name')
def get_device_id_from_device_name(device_name):
    device = request.json(device_name)
    device_id = data_access.get_device_id_by_name(device)
    return device_id

@app.route('/devices/String:device_id')
def getDevice(device_id):
    id = request.json(device_id)
    return data_access.get_device(id)

@app.route('/devices/String:device_id')
def deleteDevice(device_id):
    id = request.json(device_id)
    data_access.delete_device(id)

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0', port='5400')