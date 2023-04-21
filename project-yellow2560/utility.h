#ifndef UTILITY_H
#define UTILITY_H

#include <Arduino.h>
#include <math.h>

double perpendicularDistance(double lat1, double lon1, double lat2, double lon2, float lat3, float lon3);
double toRadians(double degrees);

#endif