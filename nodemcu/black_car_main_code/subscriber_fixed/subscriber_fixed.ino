#include <Arduino.h>
/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

// int gpio = 12;
// void setup(){
//   pinMode(gpio, OUTPUT);
// }

// void loop(){
//   digitalWrite(gpio, HIGH);
// }

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <String.h>
#include "mecanum_wheel_1.h"
#include "Wire.h"
#include <MPU6050_light.h>
#define MAX_MSG_LEN (128)

const char* ssid     = "RoboWifi";
const char* password = "73333449";
const char *serverHostname = "192.168.1.23";
const char *topic1 = "raspberry/imu";
const char *topic2 = "raspberry/bot";
const char* mqtt_username = "sumobot";
const char* mqtt_password = "sumobot";
unsigned long startMillis;  //some global variables available anywhere in the program
unsigned long currentMillis;
const unsigned long period = 1000;  //the value is a number of milliseconds
WiFiClient espClient;
PubSubClient client(espClient);

MPU6050 mpu(Wire);
unsigned long timer = 0;
unsigned long timer2 = 0;
double raw_angle = 0;
double angle = 0;

StaticJsonDocument<60> jsonBuffer;

double process_angle(double angle){
  if (angle > 180){
    while(angle > 180){
      angle -= 360;
    }
  } else if (angle < -180){
    while(angle < -180){
      angle += 360;
    }
  }
  return angle;
}

void connectWifi(){
  delay(10);

    // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char *msgTopic, byte *msgPayload, unsigned int msgLength) {
  startMillis = millis(); 
  if(strcmp(msgTopic,topic1)==0){
    Serial.println("Topic IMU");
  // copy payload to a static string
  static char message[MAX_MSG_LEN + 1];
  if (msgLength > MAX_MSG_LEN) {
    msgLength = MAX_MSG_LEN;
  }
  strncpy(message, (char *)msgPayload, msgLength);
  message[msgLength] = '\0';
  String myString = String(message); 

  if(myString[0] == '1'){
    Serial.println("Turn anticlockwise");
    turnAntiClockwise();
  } else if (myString[0] == '2') {
    Serial.println("Turn clockwise");
    turnClockwise();
  } else {
    allStop();
  }
  }

  else if (strcmp(msgTopic,topic2)==0) {
    Serial.println("Topic BOT");
     static char message[MAX_MSG_LEN + 1];
  if (msgLength > MAX_MSG_LEN) {
    msgLength = MAX_MSG_LEN;
  }
  strncpy(message, (char *)msgPayload, msgLength);
  message[msgLength] = '\0';

  //  Serial.printf("topic %s, message received: %s\n", msgTopic, message);
  DeserializationError err = deserializeJson(jsonBuffer, msgPayload);
  //  JsonObject& root = jsonBuffer.parseObject(msgPayload);
  if (err) {
    Serial.print(F("deserializeJson() failed with code "));
    Serial.println(err.c_str());
  }
  int action = jsonBuffer["move"];
  Serial.println(action);
  switch (action) {
    case 0:
      allStop();
      Serial.println("Receive: Stoppp");
      break;
    case 1:
      // turn left
      moveLeft();
      Serial.println("Receive: left");
      break;
    case 2:
      // turn right
      moveRight();
      Serial.println("Receive: right");
      break;
    case 3:
      // forward
      Serial.println("Receive: 4wards");
      moveForwards();
      break;
    case 4:
      // backward
      Serial.println("Receive: backwards");
      moveBackwards();
      break;
    case 5:
      // diagonalUpRight
      Serial.println("Receive: UpRight");
      diagonalUpRight();
      break;
    case 6:
      // diagonalUpLeft
      Serial.println("Receive: upleft");
      diagonalUpLeft();
      break;
    case 7:
      // diagonaldownright
      Serial.println("Receive: downright");
      diagonalDownRight();
      break;
    case 8:
      // diagonalDownLeft
      Serial.println("Receive: downleft");
      diagonalDownLeft();
      break;
    case 9:
      // turnClockwise
      Serial.println("Receive: clockwise");
      turnClockwise();
      break;
    case 10:
      // turnAntiClockwise
      Serial.println("Receive: anticlockwise");
      turnAntiClockwise();
      break;
    default:
      allStop();
      break;
    }
  }
}

void setup()
{
  Serial.begin(115200);
  pinMode(inLF1, OUTPUT);
  pinMode(inLF2, OUTPUT);
  pinMode(inRF1, OUTPUT);
  pinMode(inRF2, OUTPUT);
  pinMode(inLB1, OUTPUT);
  pinMode(inLB2, OUTPUT);
  pinMode(inRB1, OUTPUT);
  pinMode(inRB2, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(19, OUTPUT);
  pinMode(18, OUTPUT);
  pinMode(5, OUTPUT);

  // Turn off motors - Initial state
  digitalWrite(inLF1, LOW);
  digitalWrite(inLF2, LOW);
  digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, LOW);
  digitalWrite(inLB1, LOW);
  digitalWrite(inLB2, LOW);
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, LOW);
  digitalWrite(23, HIGH);
  digitalWrite(19, HIGH);
  digitalWrite(18, HIGH);
  digitalWrite(5, HIGH);
  connectWifi();
  client.setServer(serverHostname, 1883);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT Broker!");
    if (client.connect("ESP3", mqtt_username, mqtt_password)) {
      Serial.println("Connected");
    }

    else {
      Serial.println("Failed to connect");
      Serial.println(client.state());
      delay(200);
    }
  }

  client.subscribe(topic1);
  client.subscribe(topic2);

  Wire.begin();
  
  byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");
}



void loop()
{
  if (!client.connected()) {
     client.connect("ESP3", mqtt_username, mqtt_password);
     Serial.println("Connecting to MQTT client");
   }
  mpu.update();
  if((millis()-timer)>10){ // print data every 10ms
  raw_angle = mpu.getAngleZ();
  angle = process_angle(raw_angle);
  // Serial.print("\tZ : ");
  // Serial.println(angle);
  if((angle > 20 || angle < -20)){
    // Serial.println("will publish");
    if(angle > 20){
      //1 for cw, 2 for anticw
      client.publish("raspberry/imu", "1"); 
    } else {
      client.publish("raspberry/imu", "2"); 
    }
    timer2 = millis();
    }
   else {
    client.publish("raspberry/imu", "0"); 
   }
   timer = millis(); 
  }
  currentMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started)
  if (currentMillis - startMillis >= period)  //test whether the period has elapsed
  {
    // allStop();
    // Serial.println("Timeout: Stoppp");
  }
  client.loop();
}
