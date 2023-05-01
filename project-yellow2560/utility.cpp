/* Utility
-
*/

#include "utility.h"

#define EARTH_RADIUS 6371000  // Earth's radius in meters


//In order to know the distance of a GPS point (current position of the device) from a line (formed by two GPS points)
// It's necessary to use the Haversine Formula to determinate the spherical distance between these points.
    /*
    https://en.wikipedia.org/wiki/Haversine_formula
    */
//The function determinates the distance from the lapMark (lat1 and lon1) to the current GPS possition (lat2 and lon2)
double getSphericalDistance(double lat1, double lon1, float lat2, float lon2){
  
  double dLat = toRadians(lat2 - lat1);
  double dLon = toRadians(lon2 - lon1);
  double a = sin(dLat/2) * sin(dLat/2) + cos(toRadians(lat1)) * cos(toRadians(lat2)) * sin(dLon/2) * sin(dLon/2);
  double c = 2 * atan2(sqrt(a), sqrt(1-a));
  double distance = EARTH_RADIUS * c;
  return distance;
}


//Calculates the radians from decimal degrees
double toRadians(double degrees) {
  return degrees * M_PI / 180.0;
}
