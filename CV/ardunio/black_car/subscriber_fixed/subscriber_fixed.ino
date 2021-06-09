#include <ESP8266WiFi.h> 
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "mecanum_wheel_1.h"
#define MAX_MSG_LEN (128)


const char* ssid = "RoboWifi";
const char* password = "73333449";
const char *serverHostname = "192.168.1.22";
// const IPAddress serverIPAddress(192, 168, 1, 3);
const char *topic = "rl/movement";
const char* mqtt_username = "sumobot";
const char* mqtt_password = "sumobot";
WiFiClient espClient;
PubSubClient client(espClient);

StaticJsonDocument<60> jsonBuffer;

void setup() {

  // Set all the motor control pins to outputs

  pinMode(inLF1, OUTPUT);
  pinMode(inLF2, OUTPUT);
  pinMode(inRF1, OUTPUT);
  pinMode(inRF2, OUTPUT);
  pinMode(inLB1, OUTPUT);
  pinMode(inLB2, OUTPUT);
  pinMode(inRB1, OUTPUT);
  pinMode(inRB2, OUTPUT);
  
  // Turn off motors - Initial state
  digitalWrite(inLF1, LOW);
  digitalWrite(inLF2, LOW);
  digitalWrite(inRF1, LOW);
  digitalWrite(inRF2, LOW);
  digitalWrite(inLB1, LOW);
  digitalWrite(inLB2, LOW);
  digitalWrite(inRB1, LOW);
  digitalWrite(inRB2, LOW);
 
  // Configure serial port for debugging
  Serial.begin(115200);
  // Initialise wifi connection - this will wait until connected
  connectWifi();
  // connect to MQTT server  
client.setServer(serverHostname, 1883);
client.setCallback(callback);

while (!client.connected()) {
    Serial.println("Connected to MQTT Broker!");
    
  if(client.connect("ESP", mqtt_username, mqtt_password)){
    Serial.println("connectd");
  }

  else{
    Serial.println("failed");
    Serial.println(client.state());
    delay(200);
  }
    
  }

  client.subscribe(topic);
  
}

void loop() {
    client.loop();
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

void callback(char *msgTopic, byte *msgPayload, unsigned int msgLength) {
  // copy payload to a static string
static char message[MAX_MSG_LEN+1];
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
  int move = jsonBuffer["move"];
  int cw = jsonBuffer["cw"];
  Serial.println(move);
  if(move ==1 && cw == 1)
    moveFdSlow();
  else if(move == 1 && cw == 0)
    moveBdSlow();
  else if (move == 0)
    allStop();

}
