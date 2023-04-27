#include <U8g2lib.h>      //OLED
#include <Wire.h>         //I2C (SDA-SCL for OLED)
#include <Adafruit_GPS.h> //GPS
#include <SPI.h>          // SPI (MISO/MOSI for SD Card reader)

#include "mySD.h"
#include "utility.h"
#include "mySensors.h"

//Serial port for GPS (TX3(14), RX3(15))
#define GPSSerial Serial3

//Miliseconds displaying the splash screen
#define SPLASH_SCREEN_TIME 2000

//Threshold in GPS COORDINATES for the lapLine
#define DISTANCE_TO_LAPLINE_THRESHOLD 3

//BUTTONS
#define BUTTON_MOVE_PIN 19
#define BUTTON_SELECT_PIN 2
#define BUTTON_BACK_PIN 3


//GPS object initiation with selected Serial port
Adafruit_GPS GPS(&GPSSerial);

//GPS readings storage
char c;
String lapGPSpoints[4];
bool lapLineRecorded = false;

//GPS current info to display
String currentLatDeg;
String currentLonDeg;
String currentSat;

//OLED display object
U8X8_SH1106_128X64_NONAME_HW_I2C oled(U8X8_PIN_NONE);

//MENU
int menu_level = 0;
int setupCircuit_subMenu_level = 0;
bool subMenu = false;
bool activateGPS = false;
bool showSensorDataSubMenu = false;

//GLOBAL System Status String variables
extern String ssGPS = "GPS ?";
extern String ssGSM = "GSM ?";

//RUN
bool isRunning = false;
unsigned long runStartTime = 0;
unsigned long runElapsedTime = 0;
bool runStopWatchRunning = false;
float prevLat = 0.0;
float prevLon = 0.0;
int lapCount = 0;
int debounceTime = 200;

//Buttons
volatile unsigned long nowPush = 0;
volatile unsigned long lastPush = 0;
volatile unsigned long timeGap = 0;
volatile bool moveButton_pressed = false;
volatile bool selectButton_pressed = false;
volatile bool backButton_pressed = false;



//MAIN SETUP
//--------------------------------------------------------------------------------------------------
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

  setupOLED();

  setupGPS();
  setupSD();

  //Check if there's an existing lapLine in the json file
  String* strptr = getLapLineJsonPoints();
  
  if(strptr[0] != "empty"){
    lapGPSpoints[0] = strptr[0];
    lapGPSpoints[1] = strptr[1];
    lapGPSpoints[2] = strptr[2];
    lapGPSpoints[3] = strptr[3];
    Serial.println("Previous lapLine found!");
    lapLineRecorded = true;
  }else{
    Serial.println("No previous lapLine found!");    
  }  

  setupMMA8451();
  setupBME280();
}



// MOVEMENT THROUGH THE MENUS
//--------------------------------------------------------------------------------------------------
//Move Button
void menuGUI_move(){
  
  if(!subMenu){
    menu_level++;

    if(menu_level == 7){
      menu_level = 1;
    }

    displayMainMenu();
  }
  //Inside setup circuit
  else if(menu_level==2){
    setupCircuit_subMenu_level++;

    if(setupCircuit_subMenu_level == 3){
      setupCircuit_subMenu_level = 0;
    }

    displaySubMenuSetupCircuit();
  }
  //Inside RUN
  else if(menu_level==3){
    //Nothing, there's just one option to move to
  }
}


//Select Button (Menu selection -> SubMenu) or (SubMenu -> SubMenu Action)
void menuGUI_select(){

  if(!subMenu){
    oled.clear();

    switch (menu_level){
    //Splash Screen
    case 0:
      //Do nothing
      break;
    
    //>> System Status
    case 1:
      displaySubMenuSystemStatus();
      break;

    //>> Setup Circuit
    case 2:
      displaySubMenuSetupCircuit();    
      break;

    //>> Run
    case 3:
      displaySubMenuRun();
      break;

    //>> GPS Info
    case 4:
      displaySubMenuGPSinfo(); 
      break;

    //>> GSM Info
    case 5:
      displaySubMenuGSMinfo();
      break;
    
    //>> Sensor data
    case 6:
      displaySubMenuSensorData();
      break; 
    }

  }else{

    //Inside Setup Circuit
    if(menu_level==2){
      if(setupCircuit_subMenu_level == 0){
        Serial.print("P1: ");
        //Get P1 GPS coordinates
        lapGPSpoints[0] = currentLatDeg;
        lapGPSpoints[1] = currentLonDeg;
        Serial.print(currentLatDeg);
        Serial.print("  ");
        Serial.println(currentLonDeg);

      }else if (setupCircuit_subMenu_level == 1){
        Serial.print("P2: ");
        //Get P2 GPS coordinates
        lapGPSpoints[2] = currentLatDeg;
        lapGPSpoints[3] = currentLonDeg;
        Serial.print(currentLatDeg);
        Serial.print("  ");
        Serial.println(currentLonDeg);

      }else if (setupCircuit_subMenu_level == 2){
        Serial.println("SAVED");
        //create JSON
        createLapLineJson(lapGPSpoints);
        lapLineRecorded = true;
      }

      displaySubMenuSetupCircuit();
    }

    //Inside RUN
    if(menu_level==3){
      
      //Check lapLine
      if(lapLineRecorded){
        if(!isRunning){

          //clean previous laps and times
          lapCount = 0;
          prevLat = 0.0;
          prevLon = 0.0;

          //Start run
          isRunning = true;
        
        }else{
          //Stop run
          stopRun();
          //save?

          isRunning = false;
          displaySubMenuRun();
        }
      }else{
        //Do nothing if there's no lapline set
        Serial.println("NO LAPLINE!");
      }
    }

    
  }

  subMenu = true;
}


//Back Button
void menuGUI_back(){
  
  //Moves back to the main menu
  if(subMenu && !isRunning){
    menu_level = 1;
    setupCircuit_subMenu_level = 0;
    subMenu = false;
    displayMainMenu();
  }
  
}



//--------------OLED SCREEN---------------
//OLED Screen setup
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
  Serial.println("OLED OK");
}

// GUI
//--------------------------------------------------------------------------------------------------
//Controls MAIN Menu GUI
void displayMainMenu(){
  oled.clear();

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
      oled.drawString(0, 7, "Sensor data");
      break;

    //Page2
    // >> GSM Info
    case 5:
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(3, 1, " MAIN MENU");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "GPS Info");
      oled.drawString(0, 5, "\xbb GSM Info");
      oled.drawString(0, 7, "Sensor data");
      break;
    
    //Page2
    // >> Sensor data
    case 6:
      oled.setFont(u8x8_font_5x7_f);
      oled.drawString(3, 1, " MAIN MENU");
      oled.setFont(u8x8_font_amstrad_cpc_extended_f);
      oled.drawString(0, 3, "GPS Info");
      oled.drawString(0, 5, "GSM Info");
      oled.drawString(0, 7, "\xbb Sensor data");
      break;
  }

}

//System Status SUBMENU
void displaySubMenuSystemStatus(){
  oled.clear();
  oled.setFont(u8x8_font_5x7_f);
  oled.drawString(2, 1, "System Status");
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  oled.setCursor(0, 3);
  oled.print(ssGPS);
  oled.setCursor(0, 4);
  oled.print(ssGSM);
  oled.setCursor(0, 5);
  oled.print(ssSD);
  oled.setCursor(0, 6);
  oled.print(ssMMA8451);
  oled.setCursor(0, 7);
  oled.print(ssBME280);
}

//Setup Circuit SUBMENU
void displaySubMenuSetupCircuit(){
  oled.clear();
  oled.setFont(u8x8_font_5x7_f);
  oled.setInverseFont(1);
  oled.drawString(2, 1, "Setup Circuit");
  oled.setInverseFont(0);
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  switch(setupCircuit_subMenu_level){
    case 0:
      oled.setCursor(0, 2);
      oled.print("\xbb P1: "+lapGPSpoints[0]);
      oled.setCursor(0, 3);
      oled.print("\t\t\t\t\t\t"+lapGPSpoints[1]);

      oled.setCursor(0, 4);
      oled.print("P2: "+lapGPSpoints[2]);
      oled.setCursor(0, 5);
      oled.print("\t\t\t\t\t\t"+lapGPSpoints[3]);

      oled.drawString(0, 7, "Confirm"); 
      break;
    
    case 1:
      oled.setCursor(0, 2);
      oled.print("P1: "+lapGPSpoints[0]);
      oled.setCursor(0, 3);
      oled.print("\t\t\t\t\t\t"+lapGPSpoints[1]);

      oled.setCursor(0, 4);
      oled.print("\xbb P2: "+lapGPSpoints[2]);
      oled.setCursor(0, 5);
      oled.print("\t\t\t\t\t\t"+lapGPSpoints[3]);
      
      oled.drawString(0, 7, "Confirm"); 
      break;

    case 2:
      oled.setCursor(0, 2);
      oled.print("P1: "+lapGPSpoints[0]);
      oled.setCursor(0, 3);
      oled.print("\t\t\t\t\t\t"+lapGPSpoints[1]);

      oled.setCursor(0, 4);
      oled.print("P2: "+lapGPSpoints[2]);
      oled.setCursor(0, 5);
      oled.print("\t\t\t\t\t\t"+lapGPSpoints[3]);
      
      oled.drawString(0, 7, "\xbb Confirm"); 
      break;
  }
  
}

//RUN SUBMENU
void displaySubMenuRun(){
  oled.clear();
  oled.setFont(u8x8_font_5x7_f);
  oled.setInverseFont(1);
  oled.drawString(6, 1, "RUN");
  oled.setInverseFont(0);
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  //No Running
  if(!isRunning){
    
    oled.setCursor(0, 2);
    if(lapLineRecorded){
      oled.print("LapLine: \tok");
    }else{
      oled.print("LapLine: \tX");
    }
    
    oled.setCursor(0, 4);
    oled.print("\xbb Start");

    oled.setCursor(0, 6);
    oled.print("Time: " + getRunStopWatchTimeString());
    
    oled.setCursor(0, 7);
    oled.print("Laps: " + String(lapCount));
  }
  //Running
  else{
    oled.setCursor(0, 2);
    oled.print("LapLine: ok");

    oled.setCursor(0, 4);
    oled.print("\xbb Stop");

    oled.setCursor(0, 6);
    oled.print("Time: " + getRunStopWatchTimeString());
    
    oled.setCursor(0, 7);
    oled.print("Laps: " + String(lapCount));
  }

}

//GPS info SUBMENU
void displaySubMenuGPSinfo(){

  oled.clear();
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
    oled.drawString(0, 5, "No fix");
  }

}

//GSM info SUBMENU
//TODO
void displaySubMenuGSMinfo(){
  oled.clear();
  oled.setFont(u8x8_font_5x7_f);
  oled.drawString(4, 1, "GSM Info");
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);
  oled.drawString(0, 3, "1");
  oled.drawString(0, 5, "2");
  oled.drawString(0, 7, "3");
}

//Sensor Data SUBMENU
void displaySubMenuSensorData(){

  float* accelerationReading = getCurrentAccelerationReading();

  oled.clear();
  oled.setFont(u8x8_font_5x7_f);
  oled.drawString(2, 1, "Sensor data");
  oled.setFont(u8x8_font_amstrad_cpc_extended_f);

  oled.setCursor(0, 3);
  oled.print("X: " + String(accelerationReading[0]));
  oled.setCursor(0, 4);
  oled.print("Y: " + String(accelerationReading[1]));
  oled.setCursor(0, 5);
  oled.print("Z: " + String(accelerationReading[2]));

  oled.setCursor(0, 6);
  oled.print("Temp: " + String(getCurrentTemperature()) + char(176)+"C");
  oled.setCursor(0, 7);
  oled.print("Alt: " + String(getCurrentAltitude()) + "m");
  
  delay(3000);
}



//--------------GPS---------------
//GPS setup
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

void updateGPSinfo(){
  currentLatDeg = String(GPS.latitudeDegrees, 5);
  currentLonDeg = String(GPS.longitudeDegrees, 5);
  currentSat = "Sat:" + String(GPS.satellites);
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
//Builds the current time String with HH:MM:SS format
String timeLineConstruction(){
  //HH:MM:SS
  String timeLine = "";

  if (GPS.hour < 10 + 2) { 
    timeLine += "0"; 
  }
  timeLine += String(GPS.hour + 2, DEC);
  
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

//Buils the String line that will be send to be logged
//TODO: add current lap
String logDataLineConstruction(){

  float* accelerationReading = getCurrentAccelerationReading();

  String logLine = "";

  //time,satellites,speed,lat,lon,x,y,z,temp,alt

  logLine += timeLineConstruction();
  logLine += ",";
  logLine += String(GPS.satellites);
  logLine += ",";
  logLine += String(GPS.speed);
  logLine += ",";
  logLine += String(GPS.latitudeDegrees, 5);
  logLine += ",";
  logLine += String(GPS.longitudeDegrees, 5);
  logLine += ",";
  logLine += String(accelerationReading[0]);
  logLine += ",";
  logLine += String(accelerationReading[1]);
  logLine += ",";
  logLine += String(accelerationReading[2]);
  logLine += ",";
  logLine += String(getCurrentTemperature());
  logLine += ",";
  logLine += String(getCurrentAltitude());

  return logLine;
}


// MAIN LOOP
//--------------------------------------------------------------------------------------------------
void loop(){

  //BUTTONS
  // Move Button
  if(moveButton_pressed){
    moveButton_pressed = false;
    menuGUI_move();
  }

  // Select Button
  if (selectButton_pressed) {
    selectButton_pressed = false;
    menuGUI_select();

    //Check if GPS is required for the submenu selected (CircuitSetup, Run and GPS info)
    if(subMenu && (menu_level==2 || menu_level==3 || menu_level==4)){
      activateGPS = true;
    }

    //Check if the user is inside the Sensor data submenu
    if(subMenu && menu_level==6){
      showSensorDataSubMenu = true;
    }

  }
  
  // Back Button
  if (backButton_pressed) {
    backButton_pressed = false;
    menuGUI_back();

    if(!subMenu){             
      activateGPS = false;
      showSensorDataSubMenu = false;    
    }
  }

  //FLAGS CHECK
  // If this flag is true the SensorDataSubmenu needs to be refreshed on each main loop iteration
  if(showSensorDataSubMenu){
    displaySubMenuSensorData();
  }

  // If this flag is true the GPS parsing must be active
  if(activateGPS){
    parseGPS();
  }

  // If this flag is true the system has to initiate and manage the stopwatch and lapline checking each loop iteration
  if(isRunning){

    //Stopwatch
    if(!runStopWatchRunning){
      //Activate and reset the stopwatch
      runStopWatchRunning = true;
      runElapsedTime = 0;
      runStartTime = 0;
      runStartTime = millis();
    }

    if(runStopWatchRunning){
      //The Run has been stopped, save the total elapsed time 
      runElapsedTime = millis() - runStartTime;
    }


    //LapLine Checking
    float currentLat = GPS.latitudeDegrees;
    float currentLon = GPS.longitudeDegrees;

    //Check if the system has moved from one side of the lap line to the other
    double distance1 = getSphericalDistance(lapGPSpoints[0].toDouble(), lapGPSpoints[1].toDouble(), lapGPSpoints[2].toDouble(), lapGPSpoints[3].toDouble(), currentLat, currentLon);
    double distance2 = getSphericalDistance(lapGPSpoints[0].toDouble(), lapGPSpoints[1].toDouble(), lapGPSpoints[2].toDouble(), lapGPSpoints[3].toDouble(), prevLat, prevLon);

    Serial.print("Current distance from lapLine: ");
    Serial.println(distance1);
    Serial.print("Previous distance from lapLine: ");
    Serial.println(distance2);


    if(distance1 < DISTANCE_TO_LAPLINE_THRESHOLD && distance2 > DISTANCE_TO_LAPLINE_THRESHOLD){
      //NEW LAP
      lapCount++;
      Serial.println("LAPS: ");
      Serial.println(lapCount);
    }

    prevLat = currentLat;
    prevLon = currentLon;

    displaySubMenuRun();

    String logDataLine = logDataLineConstruction();
    logInSD(logDataLine);
  }

//END MAIN LOOP
}


//Generates a String representing the current elapsed time since the run started 
String getRunStopWatchTimeString(){
  String runStopWatchTimeString = "";

  int min = (runElapsedTime / 60000) % 60;
  int sec = (runElapsedTime / 1000) % 60;

  if (min < 10) {
    runStopWatchTimeString += "0";
  }

    runStopWatchTimeString += min;
    runStopWatchTimeString += ":";

  if (sec < 10) {
    runStopWatchTimeString += "0";
  }

  runStopWatchTimeString += sec;

  return runStopWatchTimeString;
}


// Called once the user stops the current run
void stopRun(){
  runStopWatchRunning = false;
  runElapsedTime = millis() - runStartTime;
}


void parseGPS(){
  readGPS();

  if(GPS.fix==1){
    updateGPSinfo();
    
    //Inside GPS info
    if(menu_level==4){
      displaySubMenuGPSinfo();
    }
    
    //String logDataLine = logDataLineConstruction();
    //logInSD(logDataLine);

  }else{
    //NO FIX
  }

}

// Move button Interrupt Service Routine
void moveButton_isr() {

  nowPush = millis();
  timeGap = nowPush - lastPush;
  
  if (timeGap > debounceTime) {
    moveButton_pressed = true;
  }
  lastPush = nowPush;
}

// Select button Interrupt Service Routine
void selectButton_isr() {

  nowPush = millis();
  timeGap = nowPush - lastPush;
  
  if (timeGap > debounceTime) {
    selectButton_pressed = true;  
  }
  lastPush = nowPush;
}

// Back button Interrupt Service Routine
void backButton_isr() {

  nowPush = millis();
  timeGap = nowPush - lastPush;
  
  if (timeGap > debounceTime) {
  backButton_pressed = true; 
  }
  lastPush = nowPush;
}

