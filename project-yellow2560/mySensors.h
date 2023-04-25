#ifndef MYSENSORS_H
#define MYSENSORS_H

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_BME280.h>

extern String ssMMA8451;
extern String ssBME280;

void setupMMA8451();
void setupBME280();
float* getCurrentAccelerationReading();
float getCurrentTemperature();
float getCurrentAltitude();

#endif