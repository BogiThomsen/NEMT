from flask import Flask, request, make_response
import requests

app = Flask(__name__)

# Make use of the following response codes
# return make_response('Ok', 200)
# return make_response('Created', 201)
# return make_response('Bad Request', 400)
# return make_response('Unauthorized', 401)
# return make_response('Forbidden', 403)
# return make_response('Not Found', 404)
# return make_response('Internal Server Error', 500)
# return make_response('Service Unavailable', 503)

@app.route('/v1/users', methods=['POST'])
def users():
    # Redirect to Core service
    pass

@app.route('/v1/users/<string:id>', methods=['GET', 'PUT'])
def users_id(id):
    if request.method == 'GET':
        # Redirect to Core service
        pass
    else:
        # Redirect to Core service
        pass

@app.route('/v1/users/<string:id>/availableDevices', methods=['GET'])
def users_id_available_devices(id):
    # Redirect to Core service
    pass

@app.route('/v1/users/<string:id>/rules', methods=['GET'])
def users_id_rules(id):
    # Redirect to Core service
    pass

@app.route('/v1/devices', methods=['GET', 'POST'])
def devices():
    if request.method == 'GET':
        # Query parameter page=:p used for pagination
        # Redirect to Core service
        pass
    else:
        # Redirect to Core service
        pass

@app.route('/v1/devices/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def devices_id(id):
    if request.method == 'GET':
        # Redirect to Core service
        pass
    elif request.method == 'PUT':
        # Redirect to Core service
        pass
    else:
        # Redirect to Core service
        pass

@app.route('/v1/devices/<string:id>/rules', methods=['GET'])
def devices_id_rules(id):
    # Redirect to Core service
    pass

@app.route('/v1/rules', methods=['POST'])
def rules():
    # Redirect to Core service
    pass

@app.route('/v1/rules/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def rules_id(id):
    if request.method == 'GET':
        # Redirect to Core service
        pass
    elif request.method == 'PUT':
        # Redirect to Core service
        pass
    else:
        # Redirect to Core service
        pass

if __name__ == "__main__":
  app.run(debug=True)
