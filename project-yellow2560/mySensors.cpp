/*  Adafruit's MMA8451 - Accelerometer
    BME/BMP280 - Pressure and temeperature sensor
*/

#include "mySensors.h"

//Standard sea-level pressure measured in hPa
#define SEALEVELPRESSURE_HPA (1013.25)

//MMA8451 object
Adafruit_MMA8451 mma = Adafruit_MMA8451();
String ssMMA8451 = "?";

//BME280 object
Adafruit_BME280 bme;
String ssBME280 = "?";




//Setup for the MMA8451 Accelerometer
void setupMMA8451(){

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    ssMMA8451 = "MMA8451 FAIL";
    while (1);
  }

  mma.setRange(MMA8451_RANGE_2_G);
  ssMMA8451 = "MMA8451 Ok";
}


//Setup for the BME/BMP280 sensor
void setupBME280(){
  
  unsigned status = bme.begin(BME280_ADDRESS_ALTERNATE);  
  
  if (!status) {
    Serial.println("Could not find BME280 sensor, check wiring, address, sensor ID!");
    ssBME280 = "BME280 FAIL";
    while (1) delay(10);
  }

  ssBME280 = "BME280 Ok";
}


//Returns the current reading from MMA8451 Accelerometer
float* getCurrentAccelerationReading(){
  static float accelerationReading[3];

  sensors_event_t event; 
  mma.getEvent(&event);

  accelerationReading[0] = event.acceleration.x;
  accelerationReading[1] = event.acceleration.y;
  accelerationReading[2] = event.acceleration.z;

  return accelerationReading;
}


//Returns the current temperature measured by BME/BMP280
float getCurrentTemperature(){
  return bme.readTemperature();
}


//Returns the current altite calculated by BME/BMP280
float getCurrentAltitude(){
  return bme.readAltitude(SEALEVELPRESSURE_HPA);
}


