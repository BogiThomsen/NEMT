#include "coap.h"
#include "nemt.h"


// CoAP client response callback
void callback_action(CoapPacket &packet, IPAddress ip, int port);

void InvokeAction(String name);


int sensorCount = 0;
int actionCount = 0;

Coap coap;

long int currentTime = millis();

IPAddress serverIP = IPAddress(172, 31, 91, 180);
String deviceID = "1234:567:89:1234:56";

struct Sensor
{
  String name;
  String value;
};

struct Action{
  String name;
  void (*function)();
};


Sensor sensors[100];
Action actions[100];




void callback_response(CoapPacket &packet, IPAddress ip, int port) {

    char p[packet.payloadlen + 1];
    memcpy(p, packet.payload, packet.payloadlen);
    p[packet.payloadlen] = NULL;

}

void NemtServer::PutSensors(){
  for(int i = 0; i < sensorCount; i++){
    char payload[256] = "";
    strcat(payload, deviceID);
    strcat(payload, "/");
    strcat(payload, sensors[i].name);
    strcat(payload, "/");
    strcat(payload, sensors[i].value);
    coap.put(serverIP, 5683, "devices", payload);
  }
}


// CoAP server endpoint URL
void callback_action(CoapPacket &packet, IPAddress ip, int port) {

    char p[packet.payloadlen + 1];
    memcpy(p, packet.payload, packet.payloadlen);
    p[packet.payloadlen] = NULL;

    String message(p);


    coap.sendResponse(ip, port, packet.messageid, "1");

    InvokeAction(p);
}




void NemtServer::CreateSensor(String name){
  sensors[sensorCount] = Sensor{name, ""};
  ++sensorCount;
}




void NemtServer::UpdateSensor(String name, String value)
{
  for(int i = 0; i < sensorCount; i++){
    if(sensors[i].name == name){
      sensors[i].value = value;
      return;
    }
  }
}

void NemtServer::PrintSensors(){
  Serial.println("\n\n\n\n");
  for(int i = 0; i < sensorCount; i++){
    Serial.println(sensors[i].name + ": " + sensors[i].value);
  }
}


void NemtServer::start() {
    Serial.begin(9600);
    delay(3000);

    Serial.println(WiFi.localIP());


    coap.server(callback_action, "action");
    coap.response(callback_response);
    coap.start();
}

void NemtServer::CreateAction(String name, void (*function)()){
    actions[actionCount] = Action{name, (*function)};
    ++actionCount;
}


void PerformAction(void (*function)()){
  (*function)();
}



void InvokeAction(String name){
  for(int i = 0; i < sizeof(actions) / sizeof(Action); i++){
    if(actions[i].name == name){
      PerformAction(actions[i].function);
    }
  }
}



void NemtServer::loop() {

  if(millis() - currentTime > 1000){
    PutSensors();
    currentTime = millis();
  }
    delay(100);
    coap.loop();
}
