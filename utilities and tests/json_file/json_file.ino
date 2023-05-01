#include <ArduinoJson.h>
#include <SPI.h>
#include <SD.h>

const int chipSelect = 53;

void setup() {
  Serial.begin(9600);
  while (!Serial) {}

  if (!SD.begin(chipSelect)) {
    Serial.println("SD card initialization failed!");
    while (1);
  }

  if(SD.exists("data.txt")){
    SD.remove("data.txt");
  }

  String type = "lap_line";
  double latitude1 = 38.70387;
  double longitude1 = -0.47837;
  double latitude2 = 38.70388;
  double longitude2 = -0.47838;

  // create a JSON object and add latitude and longitude data
  StaticJsonDocument<128> doc;
  JsonArray lap_line = doc.createNestedArray(type);

  JsonArray lap_line_p1 = lap_line[0].createNestedArray("p1");
  lap_line_p1.add(latitude1);
  lap_line_p1.add(longitude1);

  JsonArray lap_line_p2 = lap_line[1].createNestedArray("p2");
  lap_line_p2.add(latitude2);
  lap_line_p2.add(longitude2);

  // open the file
  File dataFile = SD.open("data.txt", FILE_WRITE);

  // serialize the JSON object to the file
  serializeJson(doc, dataFile);
  dataFile.close();

  // read the file and parse the JSON object
  dataFile = SD.open("data.txt");
  StaticJsonDocument<128> doc2;
  DeserializationError error = deserializeJson(doc2, dataFile);
  dataFile.close();

  // check for parsing errors
  if (error) {
    Serial.println(error.f_str());
    return;
  }

  float lap_line_p1_lat = doc2[type][0]["p1"][0]; // 38.70388
  float lap_line_p1_lon = doc2[type][0]["p1"][1]; // -0.47838

  float lap_line_p2_lat = doc2[type][1]["p2"][0]; // 38.70387
  float lap_line_p2_lon = doc2[type][1]["p2"][1]; // -0.47837


  Serial.println(lap_line_p1_lat, 5);
  Serial.println(lap_line_p1_lon, 5);
  Serial.println(lap_line_p2_lat, 5);
  Serial.println(lap_line_p2_lon, 5);
}

void loop() {

}
