import serial
import math
import paho.mqtt.client as mqtt
import time
import json 

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

def find_quadrant(ours_x,ours_y,arena_x,arena_y):#this one is for later use
    if ours_x - arena_x >= 0 and ours_y - arena_y >= 0:
        return 1
    elif ours_x - arena_x >= 0 and ours_y - arena_y < 0:
        return 2
    elif ours_x - arena_x < 0 and ours_y - arena_y < 0:
        return 3
    else:
        return 4

while True:
    readedText = ser.readline()
    decode = readedText.decode('UTF-8')
    decode = decode.replace("\r\n", "")
    
    ours = [0,0,0,0]# x1,y1,x2,y2
    enemy = [0,0,0,0]# same as above
    arena = [0,0]#x,y
    temp_list = decode.split(',')
    if (len(temp_list) == 10):
        decode_list = temp_list
    else:
        decode_list = ["0","0","0","0","0","0","0","0","0","0"]
    
    if (len(decode_list) == 10):
        for i in range(10):
            if i<4:
                ours[i] = int(decode_list[i])
            elif 4<=i<8:
                enemy[i-4] = int(decode_list[i])
            else:
                arena[i-8] = int(decode_list[i])
    print(ours, enemy, arena)
    radius = 40 #hardcoded value
    if (ours[0]-arena[0])**2 + (ours[1]-arena[1])**2 <= 1500:# if the bot is in the circle
        if enemy[1] < arena[1] and ours[1] < arena[1]:
            print("move forward")
            payload_dict = {"cw": True, "move": True}
            payload_json = json.dumps(payload_dict)
            client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
        elif enemy[1] > arena[1] and ours[1] > arena[1]:
            print("move back")
            payload_dict = {"cw": False, "move": True}
            payload_json = json.dumps(payload_dict)
            client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
        else:
            print("dont move")
            payload_dict = {"cw": True, "move": False}
            payload_json = json.dumps(payload_dict)
            client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
    else:
        print("dont move")
        payload_dict = {"cw": True, "move": False}
        payload_json = json.dumps(payload_dict)
        client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
    
   

