from coapthon.server.coap import CoAP
from coapthon.client.helperclient import HelperClient
import requests
import validator
import json
import datetime
import sys

from coapthon.resources.resource import Resource

core_url = 'http://device-service:5400/v1'
headers = {'User-Agent': 'web-app-api', 'Content-Type': 'application/json'}
api_version = 'v1'


#Endpoint for the devices to update a value from a sensor to the database.
class updateValue(Resource):
    def __init__(self, name="updateValue", coap_server=None):
        super(updateValue, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)

    def render_PUT_advanced(self, request, response):

        result = validator.validate_device_request(request.payload)
        print(result)
        if result != "":
            response.payload = "400 - " + result
            return self, response

        split = request.payload.split("/")
        deviceToken = split[0]
        sensorName = split[1]
        value = split[2]

        data = {
            "value":value
        }

        print(value)

        response = requests.patch(core_url + '/device/' + deviceToken + "/sensors/" + sensorName, headers=headers, json=data)
        response_code = response.status_code

        if response_code == 400 or response_code == 404:
            response.payload = "{}".format(response.status_code) + " - " + response.text
        else:
            response.payload = response_code


        return self, response



class exposeSensors(Resource):
    def __init__(self, name="exponseSensors", coap_server=None):
        super(exposeSensors, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)

    def render_PUT_advanced(self, request, response):

        result = validator.validate_device_request(request.payload)
        print(result)
        if result != "":
            response.payload = result
            return self, response

        split = request.payload.split("/")
        deviceToken = split[0]
        del split[0]
        sensors = []
        for sensor in split:
            sensors.append(sensor)
        data = {}
        data['sensors'] = sensors
        json_data = json.dumps(data)

        # return requests.patch(core_url + '/devices/' + deviceToken + "/sensors/" + sensorName, headers=headers,
        # data=json_data)


        return self



class exposeActions(Resource):
    def __init__(self, name="exposeActions", coap_server=None):
        super(exposeActions, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)

    def render_PUT_advanced(self, request, response):
        result = validator.validate_device_request(request.payload)
        print(result)
        if result != "":
            response.payload = result
            return self, response

        split = request.payload.split("/")
        deviceToken = split[0]
        del split[0]
        actions = []
        for action in split:
            actions.append(action)
        data = {}
        data['actions'] = actions
        json_data = json.dumps(data)

        return self

        # return requests.patch(core_url + '/devices/' + deviceToken + "/sensors/" + sensorName, headers=headers,
        #                      data=json_data)



class CoAPServer(CoAP):
    print("pre init")
    
    def __init__(self, host, port):
        try:
            print("first")
            CoAP.__init__(self, (host, port))
            print("second")
            self.add_resource('updateValue/', updateValue())
            print("third")
            self.add_resource('exposeSensors/', exposeSensors())
            print("fourth")
            self.add_resource('exposeActions/', exposeActions())
            print("last")
        except Exception as e:
            print(e)

def outbound(host, port, value):
    print("outbound 1")
    client = HelperClient(server=(host, port))
    print("outbound 2")
    response = client.put("action", value)
    print("response is " + response.__str__)


if __name__ == '__main__':
    print("starting....")
    server = CoAPServer("0.0.0.0", 5683)
    print("coap server started")
    server.listen(10)
    print("listen is over")



