#include "mySensors.h"

//Standard pressure at sea-level measured in hPa
#define SEALEVELPRESSURE_HPA (1013.25)

//MMA8451 object
Adafruit_MMA8451 mma = Adafruit_MMA8451();
String ssMMA8451 = "?";

//BME280 object
Adafruit_BME280 bme;
String ssBME280 = "?";

void setupMMA8451(){

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    ssMMA8451 = "MMA8451 FAIL";
    while (1);
  }

  Serial.println("MMA8451 found!");
  mma.setRange(MMA8451_RANGE_2_G);
  ssMMA8451 = "MMA8451 Ok";
}


void setupBME280(){
  
  unsigned status = bme.begin(BME280_ADDRESS_ALTERNATE);  
  
  if (!status) {
    Serial.println("Could not find BME280 sensor, check wiring, address, sensor ID!");
    ssBME280 = "BME280 FAIL";
    while (1) delay(10);
  }

  Serial.println("BME280 found!");
  ssBME280 = "BME280 Ok";
}


float* getCurrentAccelerationReading(){
  static float accelerationReading[3];

  sensors_event_t event; 
  mma.getEvent(&event);

  accelerationReading[0] = event.acceleration.x;
  accelerationReading[1] = event.acceleration.y;
  accelerationReading[2] = event.acceleration.z;

  return accelerationReading;
}



float getCurrentTemperature(){
  return bme.readTemperature();
}


float getCurrentAltitude(){
  return bme.readAltitude(SEALEVELPRESSURE_HPA);
}


