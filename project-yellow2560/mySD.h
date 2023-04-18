#ifndef MYSD_H
#define MYSD_H

#include <Arduino.h>
#include <SD.h>           //SD Card reader library

extern String ssSD;

void setupSD();
void logInSD(String logDataLine);
void createLapLineJson(String gpsPoints[]);

#endif