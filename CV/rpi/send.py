
import math
import paho.mqtt.client as mqtt
import time
import json 
import numpy as np

mqtt_username = "sumobot"
mqtt_password = "sumobot"

movement = ["stop", "left", "right", "forward", "backward", "downleft", "upright", "upleft", "downright", "clockwise", "anticlockwise"]

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print("Connected")

while True:
    to_move = input("What to do\n")
    client.on_connect = on_connect
    client.connect("raspberrypi", 1883, 60)
    payload_dict = {"cw": True, "move": to_move}
    payload_json = json.dumps(payload_dict)
    print(movement[payload_dict["move"]])
    client.publish('raspberry/bot', payload=payload_json, qos = 0, retain=False)



