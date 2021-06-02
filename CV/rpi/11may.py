import serial
import math
import paho.mqtt.client as mqtt
import time
import json 
import numpy as np
from keras.models import load_model

ser=serial.Serial('/dev/ttyACM0',115200)
distance = 0
mqtt_username = "sumobot"
mqtt_password = "sumobot"

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print(1)
client.on_connect = on_connect
client.connect("raspberrypi", 1883, 60)

#load model
model = load_model('mymodel2.h5')

while True:
    readedText = ser.readline()
    decode = readedText.decode('UTF-8')
    decode = decode.replace("\r\n", "")
    
    ours = [0,0]# x1,y1,x2,y2
    enemy = [0,0]# same as above
    temp_list = decode.split(',')
    if (len(temp_list) == 4):
        decode_list = temp_list
    else:
        decode_list = ["0","0","0","0"]
    
    for i in range(4):
        if i<2:
            ours[i] = int(decode_list[i])
        else:
            enemy[i-2] = int(decode_list[i])



    
   

