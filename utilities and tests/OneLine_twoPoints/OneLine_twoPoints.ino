#define EARTH_RADIUS 6371000  // Earth's radius in meters

double getSphericalDistance(double lat1, double lon1, double lat2, double lon2, float lat3, float lon3){
  
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
  double distance = 2 * sqrt(s * (s - d12) * (s - d13) * (s - d23)) / d12;
  
  return distance;
}


//Calculates the radians from decimal degrees
double toRadians(double degrees) {
  return degrees * M_PI / 180.0;
}



void setup() {
  Serial.begin(9600);
  
  float currentLat = 38.70395;
  float currentLon = -0.47890;

  //Check if the system has moved from one side of the lap line to the other
  double distance1 = getSphericalDistance(38.70409,-0.47906, 38.70418,-0.47915, currentLat, currentLon);
  
  Serial.println(distance1);

}

void loop() {

}
