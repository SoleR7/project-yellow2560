#ifndef UTILITY_H
#define UTILITY_H

#include <Arduino.h>
#include <math.h>

double getSphericalDistance(double lat1, double lon1, float lat2, float lon2);
double toRadians(double degrees);

#endif