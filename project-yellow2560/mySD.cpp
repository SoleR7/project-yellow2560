#include "mySD.h"

//Chip Select pin for SD card reader
#define SD_CS 53

//SD card reader
String fileName = "data.csv";
File sdFile;

String ssSD = "SD ?";

void setupSD(){
  pinMode(SD_CS, OUTPUT);
  
  if(!SD.begin(SD_CS)){
    ssSD = "SD FAIL";
    while(1);
  }

  if(SD.exists(fileName)){
    SD.remove(fileName);
    ssSD = "SD REMOVED";
  }

  ssSD = "SD OK";
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
  Serial.println("JSON!");
  Serial.println(gpsPoints[0]);
  Serial.println(gpsPoints[1]);
  Serial.println(gpsPoints[2]);
  Serial.println(gpsPoints[3]);
}




