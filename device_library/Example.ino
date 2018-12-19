#include "nemt.h"

NemtServer nemt;

//User defined function specific to the usecase of this given device
void Blink(){
  for(int i = 0; i < 10; i++){
    digitalWrite(D7, HIGH);
    delay(100);
    digitalWrite(D7, LOW);
    delay(100);
  }
}

int ReadLightLevels(){
  return analogRead(A0);
}


void setup() {
//Prerequisites for the program to run
    pinMode(D7, OUTPUT);
    pinMode(A0, INPUT);

//Exposing the sensors to NEMT
    nemt.CreateSensor("Temperature");
    nemt.CreateSensor("Light");
    nemt.CreateSensor("humidity");

//Exposing actions to NEMT
    nemt.CreateAction("blink", Blink);

//Start the NEMT service
    nemt.start();
}
void loop() {

//Update the sensor values

    String temperature = String(20.0 + (random(-500, 500) / 100.0));
    String humidity = String(30.0 + (random(-1000, 1000) / 100.0));


    nemt.UpdateSensor("Temperature", temperature.substring(0, (temperature.length() -4)));
    nemt.UpdateSensor("humidity", humidity.substring(0, (humidity.length() -4)));
    nemt.UpdateSensor("Light", String(ReadLightLevels()));

//Run the NEMT service, this will keep sensor values up-to-date on the server
//And run the actions sent to this device
    nemt.loop();
}
