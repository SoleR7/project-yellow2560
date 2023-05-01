//ACCELOMETER 0x1D
//BMP 0x76

#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_BME280.h>
#include <Adafruit_Sensor.h>

#define SEALEVELPRESSURE_HPA (1013.25)


Adafruit_MMA8451 mma = Adafruit_MMA8451();
Adafruit_BME280 bme;

void setup(void) {
  Serial.begin(9600);

  if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");
  
  mma.setRange(MMA8451_RANGE_2_G);

  unsigned status = bme.begin(BME280_ADDRESS_ALTERNATE);  
  
  if (!status) {
    Serial.println("Could not find BME280 sensor, check wiring, address, sensor ID!");
    while (1) delay(10);
  }
}

void loop() {

  sensors_event_t event; 
  mma.getEvent(&event);

  /* Display the results (acceleration is measured in m/s^2) */
  Serial.print("X:"); 
  Serial.print(event.acceleration.x);
  Serial.print(",");

  Serial.print("Y:"); 
  Serial.print(event.acceleration.y);
  Serial.print(",");

  Serial.print("Z:"); 
  Serial.print(event.acceleration.z);
  //Serial.println();

  Serial.print(",");

  Serial.print("Temperature:");
  Serial.print(bme.readTemperature());
  Serial.print(",");

  Serial.print("Altitude:");
  Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));

  Serial.println();

  /*
  Serial.print("Temperature = ");
  Serial.print(bme.readTemperature());
  Serial.println(" °C");

  Serial.print("Approx. Altitude = ");
  Serial.print(bme.readAltitude(SEALEVELPRESSURE_HPA));
  Serial.println(" m");
  Serial.println();
  */


  //delay(2000);
}
