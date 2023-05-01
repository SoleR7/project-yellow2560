#ifndef MYSD_H
#define MYSD_H

#include <Arduino.h>
#include <SD.h>           // SD Card reader library
#include <ArduinoJson.h>  // JSON parser library

extern String ssSD;

void setupSD();
void logInSD(String logDataLine, bool lapLog);
void createLapMarkJson(String gpsPoint[]);
String* getLapMarkJsonPoint();

#endif