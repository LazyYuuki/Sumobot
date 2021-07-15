#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "Wire.h"
#include <MPU6050_light.h>
#define MAX_MSG_LEN (128)

const char* ssid = "RoboWifi";
const char* password = "73333449";
const char *serverHostname = "192.168.1.3";
// const IPAddress serverIPAddress(192, 168, 1, 3);
const char *topic = "raspberry/bot";
const char* mqtt_username = "sumobot";
const char* mqtt_password = "sumobot";
MPU6050 mpu(Wire);
unsigned long timer = 0;
unsigned long timer2 = 0;
WiFiClient espClient;
PubSubClient client(espClient);
double raw_angle = 0;
double angle = 0;

StaticJsonDocument<60> jsonBuffer;

void setup() {

  Wire.begin();
  // Configure serial port for debugging
  Serial.begin(115200);


  // Initialise wifi connection - this will wait until connected
  connectWifi();
  // connect to MQTT server
  client.setServer(serverHostname, 1883);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT Broker!");
    if (client.connect("ESPIMU", mqtt_username, mqtt_password)) {
      Serial.println("Connected");
    }

    else {
      Serial.println("Failed to connect");
      Serial.println(client.state());
      delay(200);
    }

  }
   byte status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(status);
  while(status!=0){ } // stop everything if could not connect to MPU6050
  
  Serial.println(F("Calculating offsets, do not move MPU6050"));
  delay(1000);
   mpu.upsideDownMounting = true; // uncomment this line if the MPU6050 is mounted upside-down
  mpu.calcOffsets(); // gyro and accelero
  Serial.println("Done!\n");
}

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

void loop() {
    if (!client.connected()) {
    connectWifi();
  }
  client.loop();
   mpu.update();
  if((millis()-timer)>10){ // print data every 10ms
  raw_angle = mpu.getAngleZ();
  angle = process_angle(raw_angle);
  Serial.print("\tZ : ");
  Serial.println(angle);
  if((angle > 10 || angle < -10) && (millis()-timer2)>500){
    Serial.println("will publish");
    if(angle > 10){
      //1 for cw, 2 for anticw
    client.publish("raspberry/imu", "1"); 
    } else {
      client.publish("raspberry/imu", "2"); 
    }
    timer2 = millis();
    }
   timer = millis(); 
  }
}

void connectWifi() {
  delay(10);
  // Connecting to a WiFi network
  Serial.print("\nConnecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(250);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected on IP address ");
  Serial.println(WiFi.localIP());
}

void connectMQTT() {
  // Wait until we're connected
  while (!client.connect(serverHostname, mqtt_username, mqtt_password)) {
    // Create a random client ID
    String clientId = "ESP8266-";
    clientId += String(random(0xffff), HEX);
    Serial.printf("MQTT connecting as client %s...\n", clientId.c_str());
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_username, mqtt_password)) {
      client.subscribe(topic);
    } else {
      Serial.println("MQTT failed, state");
      // Wait before retrying
      delay(2500);
    }
  }
}
