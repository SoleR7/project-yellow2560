#include <U8g2lib.h>  //OLED
#include <Wire.h>     //I2C (SDA-SCL)
#include <Adafruit_GPS.h> //GPS
#include <SPI.h> // SPI (MISO/MOSI)
#include <SD.h> //SD Card reader

//Serial port for GPS (TX1(18), RX1(19))
#define GPSSerial Serial1

//Chip Select pin for SD card reader
#define SD_CS 53


//GPS object initiation with selected Serial port
Adafruit_GPS GPS(&GPSSerial);

//GPS readings storage
char c;

//OLED display object
U8X8_SH1106_128X64_NONAME_HW_I2C oled(U8X8_PIN_NONE);

//SD card reader
String fileName = "data.csv";
File sdFile;



//MAIN SETUP
void setup(){
  Serial.begin(115200);

  setupOLED();
  setupGPS();
  setupSD();

}


//--------------OLED SCREEN---------------

void setupOLED(){
  //Mininum clock speed for the oled display
  Wire.setClock(10000);
  
  oled.begin();

  //Font
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  //Reverse?
  //...
  
  Serial.println("OLED OK");
}


void displayOLED(){
  oled.clearDisplay();
  oled.setCursor(0, 1);
  oled.print(String(GPS.latitudeDegrees, 4));
  
}


//--------------GPS---------------
void setupGPS(){
  
  GPS.begin(9600);

  //Amount of data that the GPS transmits
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  //GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCONLY);
  
  // 1 Hz update rate
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  
  //Antenna info  
  //GPS.sendCommand("$CDCMD,33,1*7C");
  delay(1000);
  Serial.println("GPS OK");
}


void clearGPS(){

  while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA());
  while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA());
   while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA());
}



void readGPS(){

  clearGPS();

  while(!GPS.newNMEAreceived()){
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA());
  String NMEA1 = GPS.lastNMEA();
  
   while(!GPS.newNMEAreceived()) {
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA()); //Parse that last good NMEA sentence
  String NMEA2 = GPS.lastNMEA();
  
  /*
  Serial.println(NMEA1);
  Serial.println(NMEA2);
  */

}



//--------------SD CARD READER---------------
void setupSD(){
  pinMode(SD_CS, OUTPUT);
  
  if(!SD.begin(SD_CS)){
    Serial.println("Card failed");
    while(1);
  }

  if(SD.exists(fileName)){
    SD.remove(fileName);
    Serial.println(fileName + " removed");
  }

  Serial.println("SD OK");

}


String timeLineConstruction(){
  //HH:MM:SS
  String timeLine = "";

  if (GPS.hour < 10) { 
    timeLine += "0"; 
  }
  timeLine += String(GPS.hour, DEC);
  
  timeLine += ":";

  if (GPS.minute < 10) { 
    timeLine += "0"; 
  }
  timeLine += String(GPS.minute, DEC); 

  timeLine += ":";

  if (GPS.seconds < 10) {
    timeLine += "0"; 
  }
  timeLine += String(GPS.seconds, DEC); 

  return timeLine;
}


void logInSD(){
    String logLine = "";
    sdFile = SD.open(fileName, FILE_WRITE);

    if(sdFile){
      //time,satellites,speed,lat,lon
      logLine += timeLineConstruction();
      logLine += ",";
      logLine += String(GPS.satellites);
      logLine += ",";
      logLine += String(GPS.speed);
      logLine += ",";
      logLine += String(GPS.latitudeDegrees, 4);
      logLine += ",";
      logLine += String(GPS.longitudeDegrees, 4);

      sdFile.println(logLine);

      /*
      sdFile.print(timeLineConstruction());
      sdFile.print(",");
      sdFile.print(GPS.satellites);
      sdFile.print(",");
      sdFile.print(GPS.speed);
      sdFile.print(",");
      sdFile.print(GPS.latitudeDegrees, 4);
      sdFile.print(",");
      sdFile.println(GPS.longitudeDegrees,4);*/

      sdFile.close();

      Serial.print("Saved on SD: ");
      Serial.println(logLine);

      delay(100);
      
    }else{
      Serial.println("Error openning " + fileName);
    }

}




//------------------------------------------------------------
//MAIN LOOP
void loop(){

  readGPS();

  if(GPS.fix==1){

    logInSD();
    displayOLED();
   
  }else{
    //TO CHANGE
    sdFile = SD.open(fileName, FILE_WRITE);

    if(sdFile){
      sdFile.println(GPS.lastNMEA());
      sdFile.close();
      Serial.println("saved on SD!");
    }else{
      Serial.println("Error openning " + fileName);
    }
    
  }

}



