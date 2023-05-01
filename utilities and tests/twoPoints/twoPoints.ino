#include <math.h>

#define RADIUS 6371000  // Earth's radius in meters

double toRadians(double degrees) {
  return degrees * M_PI / 180.0;
}

double haversine(double lat1, double lon1, double lat2, double lon2) {
  double dLat = toRadians(lat2 - lat1);
  double dLon = toRadians(lon2 - lon1);
  double a = sin(dLat/2) * sin(dLat/2) + cos(toRadians(lat1)) * cos(toRadians(lat2)) * sin(dLon/2) * sin(dLon/2);
  double c = 2 * atan2(sqrt(a), sqrt(1-a));
  double d = RADIUS * c;
  return d;
}

void setup() {
  Serial.begin(9600);

  double lat1 = 38.70409;  // latitude of point 1
  double lon1 = -0.47906;  // longitude of point 1
  double lat2 = 38.70395;  // latitude of point 2
  double lon2 = -0.47890;  // longitude of point 2

  double distance = haversine(lat1, lon1, lat2, lon2);

  Serial.println(distance);




}

void loop() {
}
