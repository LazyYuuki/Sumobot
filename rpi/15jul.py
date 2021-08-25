import serial
import math
import paho.mqtt.client as mqtt
import time
import json 
import numpy as np
from keras.models import load_model

movement = ["do nothing", "left", "right", "up", "down", "top right", "top left", "bottom right", "bottom left"]

ser=serial.Serial('/dev/ttyACM0',9600)
mqtt_username = "sumobot"
mqtt_password = "sumobot"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print("Connected")
client.on_connect = on_connect
client.connect("raspberrypi", 1883, 60)

#load model
model = load_model('final4.h5')

while True:
    readedText = ser.readline()
    decode = readedText.decode('UTF-8')
    decode = decode.replace("\r\n", "")
    temp_list = decode.split(',')
    if (len(temp_list) < 6):
        decode_list = [0, 0, 0, 0, 0, 0]
    else:
        decode_list = [int(i) for i in temp_list]
    #print(decode_list)
    new_list = decode_list[0:4]
    X = np.reshape(new_list, (1, 4))
    pred = model(X)
    print(decode_list)
    move = np.argmax(pred[0])
    print(movement[move])
    payload_dict = {"cw": True, "move": int(move)}
    payload_json = json.dumps(payload_dict)
    client.publish('raspberry/bot', payload=payload_json, qos = 0, retain=False)

