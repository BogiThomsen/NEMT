from coapthon.server.coap import CoAP
from coapthon.client.helperclient import HelperClient
import validator
import datetime

from coapthon.resources.resource import Resource

class updateValue(Resource):
    def __init__(self, name="updateValue", coap_server=None):
        super(updateValue, self).__init__(name, coap_server, visible=True,
                                            observable=False, allow_children=True)

    def render_PUT_advanced(self, request, response):

        result = validator.validate_device_request(request.payload)
        print(result)
        if result != "":
            response.payload = result
            return self, response

        split = request.payload.split("/")
        device = split[0]
        sensor = split[1]
        value = split[2]
        print(request.payload)
        return self



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
        device = split[0]
        sensor = split[1]
        value = split[2]
        print(request.payload)
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
            device = split[0]
            sensor = split[1]
            value = split[2]
            print(request.payload)
            return self


class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource('updateValue/', updateValue())
        self.add_resource('exposeSensors/', exposeSensors())
        self.add_resource('exposeActions/', exposeActions())

def outbound(host, port, action, value):
    client = HelperClient(server=(host, port))
    response = client.put(action, value.__str__())

def main():
    #outbound("192.168.1.128", 5683, "light", 0)

    server = CoAPServer("172.31.91.180", 5683)
    try:
        server.listen(10)
    except KeyboardInterrupt:
        print("Server Shutdown")
        server.close()
        print("Exiting...")

if __name__ == '__main__':
    main()



