#include "utility.h"

#define EARTH_RADIUS 6371000  // Earth's radius in meters


//Calculate the perpendicular distance from point 3 to the line formed by points 1 and 2
// https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
// https://en.wikipedia.org/wiki/Haversine_formula
double perpendicularDistance(double lat1, double lon1, double lat2, double lon2, float lat3, float lon3){
  
  double dLat = toRadians(lat2 - lat1);
  double dLon = toRadians(lon2 - lon1);
  double a = sin(dLat/2) * sin(dLat/2) + cos(toRadians(lat1)) * cos(toRadians(lat2)) * sin(dLon/2) * sin(dLon/2);
  double c = 2 * atan2(sqrt(a), sqrt(1-a));
  double d12 = EARTH_RADIUS * c;

  dLat = toRadians(lat3 - lat1);
  dLon = toRadians(lon3 - lon1);
  a = sin(dLat/2) * sin(dLat/2) + cos(toRadians(lat1)) * cos(toRadians(lat3)) * sin(dLon/2) * sin(dLon/2);
  c = 2 * atan2(sqrt(a), sqrt(1-a));
  double d13 = EARTH_RADIUS * c;

  dLat = toRadians(lat3 - lat2);
  dLon = toRadians(lon3 - lon2);
  a = sin(dLat/2) * sin(dLat/2) + cos(toRadians(lat2)) * cos(toRadians(lat3)) * sin(dLon/2) * sin(dLon/2);
  c = 2 * atan2(sqrt(a), sqrt(1-a));
  double d23 = EARTH_RADIUS * c;

  double s = (d12 + d13 + d23) / 2;
  double h = 2 * sqrt(s * (s - d12) * (s - d13) * (s - d23)) / d12;
  
  return h;
}


//Calculate radians from decimal degrees
double toRadians(double degrees) {
  return degrees * M_PI / 180.0;
}