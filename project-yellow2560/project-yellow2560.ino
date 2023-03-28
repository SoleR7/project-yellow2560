#include <U8g2lib.h>      //OLED
#include <Wire.h>         //I2C (SDA-SCL for OLED)
#include <Adafruit_GPS.h> //GPS
#include <SPI.h>          // SPI (MISO/MOSI for SD Card reader)
#include <SD.h>           //SD Card reader

//Serial port for GPS (TX3(14), RX3(15))
#define GPSSerial Serial3

//Chip Select pin for SD card reader
#define SD_CS 53


//Miliseconds displaying the splash screen
#define SPLASH_SCREEN_TIME 5000

//GPS object initiation with selected Serial port
Adafruit_GPS GPS(&GPSSerial);

//GPS readings storage
char c;

//GPS current info to display
String currentLatDeg;
String currentLonDeg;
String currentSat;

//OLED display object
U8X8_SH1106_128X64_NONAME_HW_I2C oled(U8X8_PIN_NONE);

//SD card reader
String fileName = "data.csv";
File sdFile;

//MENU
int menu_level = 0;
//int setupCircuit_subMenu_level = 0;
//int run_subMenu_level = 0;
bool subMenu = false;
//oled.drawString(0, 1, "\x8d \xbb \xab"); //->  >> <<
//oled.setInverseFont(1);   ON--OFF  oled.setInverseFont(0);

//System Status Strings
String ssSD = "";
String ssGPS = "";
String ssGSM = "GSM ?";


//BUTTON
#define BUTTON_MOVE_PIN 19
#define BUTTON_SELECT_PIN 2
#define BUTTON_BACK_PIN 3

int debounceTime = 200;

volatile unsigned long nowPush = 0;
volatile unsigned long lastPush = 0;
volatile unsigned long timeGap = 0;

volatile bool moveButton_pressed = false;
volatile bool selectButton_pressed = false;
volatile bool backButton_pressed = false;



//MAIN SETUP
void setup(){
  Serial.begin(115200);

// Set up the button pins as inputs
  pinMode(BUTTON_MOVE_PIN, INPUT_PULLUP);
  pinMode(BUTTON_SELECT_PIN, INPUT_PULLUP);
  pinMode(BUTTON_BACK_PIN, INPUT_PULLUP);
  
  // Enable interrupts for the buttons
  attachInterrupt(digitalPinToInterrupt(BUTTON_MOVE_PIN), moveButton_isr, FALLING);
  attachInterrupt(digitalPinToInterrupt(BUTTON_SELECT_PIN), selectButton_isr, FALLING);
  attachInterrupt(digitalPinToInterrupt(BUTTON_BACK_PIN), backButton_isr, FALLING);

  setupGPS();
  setupSD();
  setupOLED();
}





// Movement through the menu
void actionButton_singleClick(){
  
  if(!subMenu){
    Serial.println("Single Click!");
    menu_level++;

    if(menu_level == 6){
      menu_level = 1;
    }

    displayMainMenu();
  }else{
    Serial.println("Single click -> submenu");
  }

}


// Menu selection -> SubMenu
void actionButton_doubleClick(){
  
  Serial.println("Double click!");

  if(!subMenu){
    oled.clear();

    switch (menu_level){
    //Splash Screen
    case 0:
      //Do nothing
      break;
    
    //>> System Status
    case 1:
      Serial.println("System Status");
      displaySubMenuSystemStatus();
      break;

    //>> Setup Circuit
    case 2:
      Serial.println("Setup Circuit");

      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(4, 1, "GPS Info");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "1");
      oled.drawString(0, 5, "2");
      oled.drawString(0, 7, "3");     
      break;

    //>> Run
    case 3:
      Serial.println("Run");

      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(4, 1, "Run");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "1");
      oled.drawString(0, 5, "2");
      oled.drawString(0, 7, "3");
      break;

    //>> GPS Info
    case 4:
      Serial.println("GPS Info");
      displaySubMenuGPSinfo(); 
      break;

    //>> GSM Info
    case 5:
      Serial.println("GSM Info");

      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(4, 1, "GSM Info");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "1");
      oled.drawString(0, 5, "2");
      oled.drawString(0, 7, "3");
      break; 
    }

  }else{
    Serial.println("Double Click -> Submenu");
  }

  subMenu = true;
  
}


// Go back to MainMenu
void actionButton_longClick(){
  
  if(subMenu){
    Serial.println("Long click! -> Submenu");
    menu_level = 1;
    subMenu = false;
    displayMainMenu();
  }
  
}



//--------------OLED SCREEN---------------

void setupOLED(){
  //Mininum clock speed for the oled display
  Wire.setClock(10000);
  
  oled.begin();
  
  //Flip 180º
  oled.setFlipMode(1);

  //Font
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  displayMainMenu();

  delay(SPLASH_SCREEN_TIME);

  menu_level++;
  displayMainMenu();
  
  //variable ok
  Serial.println("OLED OK");
}


void displayMainMenu(){
  oled.clear();
  Serial.println(menu_level);

  switch (menu_level){
    //Splash Screen
    case 0:
      oled.drawString(0, 3, "UPV ECO-MARATHON");
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(0, 4, "Telemetry system");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      break;

    //Page1
    // >> System Status
    case 1:
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(3, 1, " MAIN MENU");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "\xbb System Status");
      oled.drawString(0, 5, "Setup Circuit");
      oled.drawString(0, 7, "Run");
      break;

    // >> Setup Circuit
    case 2:
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(3, 1, " MAIN MENU");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "System Status");
      oled.drawString(0, 5, "\xbb Setup Circuit");
      oled.drawString(0, 7, "Run");
      break;
    
    // >> Run
    case 3:
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(3, 1, " MAIN MENU");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "System Status");
      oled.drawString(0, 5, "Setup Circuit");
      oled.drawString(0, 7, "\xbb Run");
      break;
    
    //Page2
    // >> GSP Info
    case 4:
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(3, 1, " MAIN MENU");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "\xbb GPS Info");
      oled.drawString(0, 5, "GSM Info");
      break;

    //Page2
    // >> GSM Info
    case 5:
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(3, 1, " MAIN MENU");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "GPS Info");
      oled.drawString(0, 5, "\xbb GSM Info");
      break;

  }

}


void displaySubMenuSystemStatus(){
  oled.setFont(u8x8_font_5x7_f);
  oled.drawString(2, 1, "System Status");
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  oled.setCursor(0, 3);
  oled.print(ssSD);
  oled.setCursor(0, 5);
  oled.print(ssGPS);
  oled.setCursor(0, 7);
  oled.print(ssGSM);
}


void displaySubMenuGPSinfo(){
  oled.setFont(u8x8_font_5x7_f);
  oled.drawString(4, 1, "GPS Info");
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  if(GPS.fix==1){
    oled.setCursor(0, 3);
    oled.print(currentLatDeg);
    oled.setCursor(0, 5);
    oled.print(currentLonDeg);
    oled.setCursor(0, 7);
    oled.print(currentSat);

  }else{
    oled.drawString(0, 3, "No fix!");
  }

}



void updateGPSinfo(){
  currentLatDeg = String(GPS.latitudeDegrees, 4);
  currentLonDeg = String(GPS.longitudeDegrees, 4);
  currentSat = String(GPS.satellites);
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

  ssGPS = "GPS OK";
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

  GPS.parse(GPS.lastNMEA());
  String NMEA2 = GPS.lastNMEA();
  
  Serial.println(NMEA1);
  Serial.println(NMEA2);

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

  ssSD = "SD OK";
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
      //time,satellites,speed,lat,lon,lat(norm),lon(norm)
      //change decimals to 8?
      logLine += timeLineConstruction();
      logLine += ",";
      logLine += String(GPS.satellites);
      logLine += ",";
      logLine += String(GPS.speed);
      logLine += ",";
      logLine += String(GPS.latitudeDegrees, 8);
      logLine += ",";
      logLine += String(GPS.longitudeDegrees, 8);
      logLine += ",";
      logLine += String(GPS.latitude, 8);
      logLine += String(GPS.lat);
      logLine += ",";
      logLine += String(GPS.longitude, 8);
      logLine += String(GPS.lon);


      sdFile.println(logLine);
      sdFile.println(GPS.lastNMEA());
      sdFile.close();

      Serial.print("Saved on SD: ");
      Serial.println(logLine);

      //delay(100);
      
    }else{
      Serial.println("Error openning " + fileName);
    }

}




//------------------------------------------------------------
//MAIN LOOP
void loop(){

  if(moveButton_pressed){
    moveButton_pressed = false;
    actionButton_singleClick(); 
  }

  if (selectButton_pressed) {
    selectButton_pressed = false;
  }
  
  if (backButton_pressed) {
    backButton_pressed = false; 
  }

  
  readGPS();

  if(GPS.fix==1){
    updateGPSinfo();
    logInSD();
   
  }else{
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




void moveButton_isr() {

  nowPush = millis();
  timeGap = nowPush - lastPush;
  
  if (timeGap > debounceTime) {
    moveButton_pressed = true;
    Serial.println("0");
    
  }
  lastPush = nowPush;
}


void selectButton_isr() {

  nowPush = millis();
  timeGap = nowPush - lastPush;
  
  if (timeGap > debounceTime) {
    selectButton_pressed = true;
    Serial.println("1");   
  }
  lastPush = nowPush;
}


void backButton_isr() {

  nowPush = millis();
  timeGap = nowPush - lastPush;
  
  if (timeGap > debounceTime) {
  backButton_pressed = true;
  Serial.println("2");  
  }
  lastPush = nowPush;
}


