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
client.connect("192.168.1.13", 1883, 60)

payload_dict = {"cw": True, "move": 1}
payload_json = json.dumps(payload_dict)
client.publish('raspberry/bot', payload=payload_json, qos = 0, retain=False)
time.sleep(2)
payload_dict = {"cw": True, "move": 0}
payload_json = json.dumps(payload_dict)
client.publish('raspberry/bot', payload=payload_json, qos = 0, retain=False)

       


