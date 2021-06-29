#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "mecanum_wheel_1.h"
#define MAX_MSG_LEN (128)

const char* ssid = "RoboWifi";
const char* password = "73333449";
const char *serverHostname = "192.168.1.17";
// const IPAddress serverIPAddress(192, 168, 1, 3);
const char *topic = "raspberry/bot";
const char* mqtt_username = "sumobot";
const char* mqtt_password = "sumobot";
unsigned long startMillis;  //some global variables available anywhere in the program
unsigned long currentMillis;
const unsigned long period = 50;  //the value is a number of milliseconds
WiFiClient espClient;
PubSubClient client(espClient);

StaticJsonDocument<60> jsonBuffer;

void setup() {
  // Configure serial port for debugging
  Serial.begin(115200);
  // Set all the motor control pins to outputs
  startMillis = millis();  //initial start time

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

  // Initialise wifi connection - this will wait until connected
  connectWifi();
  // connect to MQTT server
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

  client.subscribe(topic);

}

void loop() {
  client.loop();
  currentMillis = millis();  //get the current "time" (actually the number of milliseconds since the program started)
  if (currentMillis - startMillis >= period)  //test whether the period has elapsed
  {
    allStop();
    Serial.println("Timeout: Stoppp");
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

void callback(char *msgTopic, byte *msgPayload, unsigned int msgLength) {
  startMillis = millis();
  // copy payload to a static string
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
      // diagonalDownLeft
      Serial.println("Receive: downleft");
      diagonalDownLeft();
      break;
    case 6:
      // diagonalUpLeft
      Serial.println("Receive: upleft");
      diagonalUpLeft();
      break;
    case 7:
      // diagonalUpRight
      Serial.println("Receive: upright");
      diagonalUpRight();
      break;
    case 8:
      // diagonalDownRight
      Serial.println("Receive: downright");
      diagonalDownRight();
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
