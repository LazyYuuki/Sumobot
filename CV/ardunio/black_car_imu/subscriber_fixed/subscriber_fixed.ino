#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <cppQueue.h>
#include "imu.h"
#define MAX_MSG_LEN (128)


const char* ssid = "RoboWifi";
const char* password = "73333449";
const char *serverHostname = "192.168.1.13";
// const IPAddress serverIPAddress(192, 168, 1, 3);
const char *topic = "raspberry/bot";
const char* mqtt_username = "sumobot";
const char* mqtt_password = "sumobot";
WiFiClient espClient;
PubSubClient client(espClient);

StaticJsonDocument<60> jsonBuffer;

cppQueue  q(sizeof(scaleddata), 2, FIFO); // Instantiate queue

float angleDisplacement = 0; // Angle of bot in Z axis

void setup() {

  Wire.begin();
  // Configure serial port for debugging
  Serial.begin(115200);

  mpu6050Begin(MPU_addr);
  setMPU6050scales(MPU_addr, 0b00000000, 0b00010000);

  // Initialise wifi connection - this will wait until connected
  connectWifi();
  // connect to MQTT server
  client.setServer(serverHostname, 1883);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT Broker!");
    if (client.connect("ESP", mqtt_username, mqtt_password)) {
      Serial.println("Connected");
    }

    else {
      Serial.println("Failed to connect");
      Serial.println(client.state());
      delay(200);
    }

  }
}

void loop() {
  scaleddata values;
  values = imuRun();
  scaleddata oldData;
  if (sizeof(q) > 1)
  {
    q.pop(&oldData);
  }
  q.push(&values);
  float timeDifference = (values.timePass - oldData.timePass);
  angleDisplacement += (timeDifference * values.GyZ) / 1000;
  Serial.println(values.GyZ);
  Serial.println(oldData.GyZ);
  Serial.println(angleDisplacement);
  String myString;
  myString = String(angleDisplacement);
  char Buf[50];
  myString.toCharArray(Buf, 50);
  client.publish("raspberry/imu", Buf);
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
