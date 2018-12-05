from flask import Flask, request

@app.route('/users', methods=['POST'])
def users():
    # Redirect to Core service
    pass

@app.route('/users/<string:id>', methods=['GET', 'PUT'])
def users_id(id):
    if request.method == 'GET':
        # Redirect to Core service
        pass
    else:
        # Redirect to Core service
        pass

@app.route('/users/<string:id>/availableDevices', methods=['GET'])
def users_available_devices(id):
    # Redirect to Core service
    pass

@app.route('/users/<string:id>/rules', methods=['GET'])
def users_rules(id):
    # Redirect to Core service
    pass

@app.route('/devices', methods=['GET', 'POST'])
def devices():
    if request.method == 'GET':
        # Query parameter page=:p used for pagination
        # Redirect to Core service
        pass
    else:
        # Redirect to Core service
        pass

@app.route('/devices/<string:id>', methods=['GET', 'PUT', 'DELETE'])
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

@app.route('/devices/<string:id>/rules', methods=['GET'])
def devices_id(id):
    # Redirect to Core service
    pass

@app.route('/rules', methods=['POST'])
def rules():
    # Redirect to Core service
    pass

@app.route('/rules/<string:id>', methods=['GET', 'PUT', 'DELETE'])
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
  app.run(debug=True,host='0.0.0.0')
