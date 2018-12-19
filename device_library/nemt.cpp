#include "coap.h"
#include "nemt.h"


// CoAP client response callback
void callback_action(CoapPacket &packet, IPAddress ip, int port);

void InvokeAction(String name);

int sensorCount = 0;
int actionCount = 0;

Coap coap;

long int currentTime = millis();

IPAddress serverIP = IPAddress(172, 31, 91, 114);
String deviceID = "172.31.91.128:5683";



struct Sensor
  {
    String name;
    String value;
  };

struct Action
  {
    String name;
    void (*function)();
  };




Sensor sensors[100];
Action actions[100];




void callback_response(CoapPacket &packet, IPAddress ip, int port) {

    char p[packet.payloadlen + 1];
    memcpy(p, packet.payload, packet.payloadlen);
    p[packet.payloadlen] = NULL;
    Serial.println("Callback");
}

void NemtServer::PutSensors(){
  for(int i = 0; i < sensorCount; i++){
    char payload[256] = "";
    strcat(payload, deviceID);
    strcat(payload, "/");
    strcat(payload, sensors[i].name);
    strcat(payload, "/");
    strcat(payload, sensors[i].value);
    coap.put(serverIP, 5683, "updateValue", payload);
  }
}


void ExposeSensors(){

  char payload[256] = "";
  strcat(payload, deviceID);

  for(int i = 0; i < sensorCount; i++){
    strcat(payload, "/");
    strcat(payload, sensors[i].name);
  }
  coap.put(serverIP, 5683, "exposeSensors", payload);
}



void ExposeActions(){
  for(int i = 0; i < actionCount; i++){
    char payload[256] = "";
    strcat(payload, deviceID);
    strcat(payload, "/");
    strcat(payload, actions[i].name);
    coap.put(serverIP, 5683, "exposeActions", payload);
  }
}


bool IsSensorsUnique(){
  for(int i = 0; i < sensorCount; i++){
    for (int j = i+1; j < sensorCount; j++) {
      if(sensors[i].name == sensors[j].name != NULL){
        return false;
      }
    }
  }
  return true;
}

bool IsActionsUnique(){
  for(int i = 0; i < actionCount; i++){
    for (int j = i+1; j < actionCount - i; j++) {
      if(actions[i].name == actions[j].name != NULL){
        return false;
      }
    }
  }
  return true;
}




// CoAP server endpoint URL
void callback_action(CoapPacket &packet, IPAddress ip, int port) {

    char p[packet.payloadlen + 1];
    memcpy(p, packet.payload, packet.payloadlen);
    p[packet.payloadlen] = NULL;

    String message(p);

    Serial.println(p);

    coap.sendResponse(ip, port, packet.messageid, "200",
                      strlen("200"), COAP_CONTENT,
                      COAP_TEXT_PLAIN, packet.token,
                      2);

//coap.sendResponse(ip, port, packet.messageid, "200");


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

    if(IsSensorsUnique() == false || IsActionsUnique() == false){
      do
      {
        Serial.println("Sensors and actions must be unqiue. Please fix this");
        Serial.print("Sensor Uniqueness: ");
        Serial.println(IsSensorsUnique(), DEC);
        Serial.print("Action Uniqueness: ");
        Serial.println(IsActionsUnique(), DEC);

        Serial.println("\n\n\n");
        delay(1000);
      } while (1);
    }

    Serial.println(WiFi.localIP());


    coap.server(callback_action, "action");
    coap.response(callback_response);
    coap.start();
/*
    for(int i = 0; i < 3; i++){
      delay(2000);
      ExposeActions();
      delay(100);
      coap.loop();
      delay(100);
      ExposeSensors();
    }
*/
}

void NemtServer::CreateAction(String name, void (*function)()){
    actions[actionCount] = Action{name, (*function)};
    ++actionCount;
}


void PerformAction(void (*function)()){
  (*function)();
}



void InvokeAction(String name){
  for(int i = 0; i < actionCount; i++){
    if(actions[i].name == name){
      PerformAction(actions[i].function);
    }
  }
}



void NemtServer::loop() {

  if(millis() - currentTime > 3000){
    PutSensors();
    currentTime = millis();
  }
    delay(100);
    coap.loop();
}
