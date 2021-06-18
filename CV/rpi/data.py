

import serial
import math
import paho.mqtt.client as mqtt
import time
import json 
import numpy as np
# from keras.models import load_model

# movement = ["do nothing", "left", "right", "up", "down", "top right", "top left", "bottom right", "bottom left"]

ser=serial.Serial('/dev/ttyACM0',115200)
mqtt_username = "sumobot"
mqtt_password = "sumobot"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print("Connected")
client.on_connect = on_connect
client.connect("raspberrypi", 1883, 60)

while True:
    readedText = ser.readline()
    decode = readedText.decode('UTF-8')
    print(decode)
    # decode = decode.replace("\r\n", "")
    # temp_list = decode.split(',')
    # if (len(temp_list) < 4):
    #     decode_list = [0, 0, 0, 0]
    # else:
    #     decode_list = [int(i) for i in temp_list]

    # X = np.reshape(decode_list, (1, 4))
    # pred = model(X)
    # print(decode_list)
    # move = np.argmax(pred[0])
    # print(movement[move])
    payload_json = json.dumps(decode)
    client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
    
   

