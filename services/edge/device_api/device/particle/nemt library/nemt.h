#ifndef nemt_h
#define nemt_h



#include "Arduino.h"

class NemtServer
{



public: void start();
public: void loop();
public: void CreateSensor(String name);
public: void CreateAction(String name, void (*function)());
public: void UpdateSensor(String name, String value);
public: void PrintSensors();
public: void PutSensors();
public: void SetupNemt(IPAddress serverIP, String deviceID);
};


#endif
