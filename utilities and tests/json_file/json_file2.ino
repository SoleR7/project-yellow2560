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

  // create a JSON object and add latitude and longitude data
  StaticJsonDocument<128> doc;
  JsonArray lap_line = doc.createNestedArray(type);
  lap_line.add(38.70388);
  lap_line.add(-0.47838);

  // open the file
  File dataFile = SD.open("data.txt", FILE_WRITE);

  // serialize the JSON object to the file
  serializeJson(doc, dataFile);
  dataFile.close();

  // read the file and parse the JSON object
  dataFile = SD.open("data.txt");
  StaticJsonDocument<256> doc2;
  DeserializationError error = deserializeJson(doc2, dataFile);
  dataFile.close();

  // check for parsing errors
  if (error) {
    Serial.println(error.f_str());
    return;
  }

  float lap_line_p1_lat = doc2[type][0]; // 38.70388
  float lap_line_p1_lon = doc2[type][1]; // -0.47838


  Serial.println(lap_line_p1_lat, 5);
  Serial.println(lap_line_p1_lon, 5);
}

void loop() {

}
