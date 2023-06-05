/* SD card reader
*/


#include "mySD.h"

//Chip Select pin for SD card reader
#define SD_CS 53

//Datalog files
String fileName_mainLog = "log.csv";
String fileName_lapLog = "laps.csv";
File sdFile;

//Lapline json file
String fileName_json = "lapMark.txt";
File sdFile_json;
String jsonHeader = "lap_mark";

String ssSD = "SD ?";




//SD Card Reader setup
void setupSD(){
  pinMode(SD_CS, OUTPUT);
  
  if(!SD.begin(SD_CS)){
    ssSD = "SD FAIL";
    Serial.println(ssSD);
    return;
  }

  if(SD.exists(fileName_mainLog)){
    SD.remove(fileName_mainLog);
  }

  if(SD.exists(fileName_lapLog)){
    SD.remove(fileName_lapLog);
  }

  ssSD = "SD Ok";
}

//Save a String in the datalog file
void logInSD(String logDataLine, bool lapLog){

  if(!lapLog){
    sdFile = SD.open(fileName_mainLog, FILE_WRITE);
  }else{
    sdFile = SD.open(fileName_lapLog, FILE_WRITE);
  }


  if(sdFile){
    sdFile.println(logDataLine);
    sdFile.close();
    delay(10);
  }else{
    Serial.println("Error openning the file to write");
  }

}

//Create the lapLine JSON file serializing the data obtained from the setupCircuit menu
void createLapMarkJson(String gpsPoint[]){

  //If there's an existing JSON file it deletes it
  if(SD.exists(fileName_json)){
    SD.remove(fileName_json);
    Serial.println("Previous lapLine deleted!");
  }


  //Create the JSON object
  StaticJsonDocument<128> jsonDoc;
  JsonArray lap_mark = jsonDoc.createNestedArray(jsonHeader);

  //Add latitude and longitude data for the lapMark
  lap_mark.add(gpsPoint[0].toFloat());
  lap_mark.add(gpsPoint[1].toFloat());


  //Open an SD file to save it
  sdFile_json = SD.open(fileName_json, FILE_WRITE);

  //Serialize the JSON object to the file
  serializeJson(jsonDoc, sdFile_json);
  sdFile_json.close();

  Serial.println("New lapMark JSON created");
}


//Obtains the data from the lapLine JSON file de-serializing the file
String* getLapMarkJsonPoint(){

  static String lapGPSpoint[2];

  if(SD.exists(fileName_json)){
    // Read the file and parse the JSON object
    sdFile_json = SD.open(fileName_json);
    StaticJsonDocument<256> jsonDoc;
    DeserializationError error = deserializeJson(jsonDoc, sdFile_json);
    sdFile_json.close();

    // Check for parsing errors
    if (error) {
      Serial.println(error.f_str());
      return;
    }

    // Extract the info from the serialized json
    float lap_mark_lat = jsonDoc[jsonHeader][0];
    float lap_mark_lon = jsonDoc[jsonHeader][1];

    lapGPSpoint[0] = String(lap_mark_lat, 5);
    lapGPSpoint[1] = String(lap_mark_lon, 5);
    
  }else{
    lapGPSpoint[0] = "empty";
  }

  return lapGPSpoint;
}

