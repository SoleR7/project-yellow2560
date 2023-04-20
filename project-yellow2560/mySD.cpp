#include "mySD.h"

//Chip Select pin for SD card reader
#define SD_CS 53

//SD card reader
// gps coordinates
String fileName = "data.csv";
File sdFile;
// lapline json
String fileName_json = "lapline.txt";
File sdFile_json;

//JSON
String jsonHeader = "lap_line";

String ssSD = "SD ?";

void setupSD(){
  pinMode(SD_CS, OUTPUT);
  
  if(!SD.begin(SD_CS)){
    ssSD = "SD FAIL";
    Serial.println(ssSD);
    while(1);
  }

  if(SD.exists(fileName)){
    SD.remove(fileName);
    ssSD = "SD CLEANED";
  }

  ssSD = "SD OK";
  Serial.println(ssSD);
}


void logInSD(String logDataLine){

  sdFile = SD.open(fileName, FILE_WRITE);

  if(sdFile){
    sdFile.println(logDataLine);
    sdFile.close();
    //delay(100);
  }else{
    Serial.println("Error openning " + fileName);
  }

}


void createLapLineJson(String gpsPoints[]){

  //DELETES PREVIOUS JSON FILE
  if(SD.exists(fileName_json)){
    SD.remove(fileName_json);
    Serial.println("Previous lapLine deleted!");
  }

  // Create the JSON object
  StaticJsonDocument<128> jsonDoc;
  JsonArray lap_line = jsonDoc.createNestedArray(jsonHeader);

  // Add latitude and longitude data for both points
  JsonArray lap_line_p1 = lap_line[0].createNestedArray("p1");
  lap_line_p1.add(gpsPoints[0]);
  lap_line_p1.add(gpsPoints[1]);

  JsonArray lap_line_p2 = lap_line[1].createNestedArray("p2");
  lap_line_p2.add(gpsPoints[2]);
  lap_line_p2.add(gpsPoints[3]);

  // Open an SD file to save it
  sdFile_json = SD.open(fileName_json, FILE_WRITE);

  // serialize the JSON object to the file
  serializeJson(jsonDoc, sdFile_json);
  sdFile_json.close();

  Serial.println("json created");
}


String* getLapLineJsonPoints(){

  static String lapGPSpoints[4];

  if(SD.exists(fileName_json)){
    // Read the file and parse the JSON object
    sdFile_json = SD.open(fileName_json);
    StaticJsonDocument<128> jsonDoc;
    DeserializationError error = deserializeJson(jsonDoc, sdFile_json);
    sdFile_json.close();

    // Check for parsing errors
    if (error) {
      Serial.println(error.f_str());
      return;
    }

    // Extract the info from the serialized json
    float lap_line_p1_lat = jsonDoc[jsonHeader][0]["p1"][0]; // p1 lat
    float lap_line_p1_lon = jsonDoc[jsonHeader][0]["p1"][1]; // p1 lon
    float lap_line_p2_lat = jsonDoc[jsonHeader][1]["p2"][0]; // p2 lat
    float lap_line_p2_lon = jsonDoc[jsonHeader][1]["p2"][1]; // p2 lon

    lapGPSpoints[0] = String(lap_line_p1_lat, 5);
    lapGPSpoints[1] = String(lap_line_p1_lon, 5);
    lapGPSpoints[2] = String(lap_line_p2_lat, 5);
    lapGPSpoints[3] = String(lap_line_p2_lon, 5);
    
  }else{
    lapGPSpoints[0] = "empty";
  }

  return lapGPSpoints;
}



