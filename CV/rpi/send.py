
import math
import paho.mqtt.client as mqtt
import time
import json 
import numpy as np

mqtt_username = "sumobot"
mqtt_password = "sumobot"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print("Connected")

client.on_connect = on_connect
client.connect("raspberrypi", 1883, 60)
while True:
    payload_dict = {"cw": True, "move": 3}
    payload_json = json.dumps(payload_dict)
    print(payload_dict)
    client.publish('raspberry/bot', payload=payload_json, qos = 0, retain=False)
       


