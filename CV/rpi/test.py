import serial
import math
import paho.mqtt.client as mqtt
import time
import json 

ser=serial.Serial('/dev/ttyACM0',115200)

while True:
    readline = ser.readlines()
    print(readline)
