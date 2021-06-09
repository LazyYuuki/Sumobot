import serial
import math
import paho.mqtt.client as mqtt
import time
import json 

ser=serial.Serial('/dev/ttyACM0',115200)
distance = 0
mqtt_username = "sumobot"
mqtt_password = "sumobot"

def on_connect(client, userdata, flags, rc):
    print(1)
    client.subscribe("outtopic")


def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload}")

def find_quadrant(ours_x,ours_y,arena_x,arena_y):#this one is for later use
    if ours_x - arena_x >= 0 and ours_y - arena_y >= 0:
        return 1
    elif ours_x - arena_x >= 0 and ours_y - arena_y < 0:
        return 4
    elif ours_x - arena_x < 0 and ours_y - arena_y < 0:
        return 3
    else:
        return 2
    

client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message
client.subscribe("outtopic")
client.connect("raspberrypi", 1883, 60)
#client.loop_start()
#time.sleep(4)
#client.loop_stop()
print("hey")

while 1:
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
                if decode_list[i] == '':
                    ours[i] = 0
                else:
                    ours[i] = int(decode_list[i])
            elif 4<=i<8:
                enemy[i-4] = int(decode_list[i])
            else:
                if decode_list[i] == '0\r0':
                    arena[i-8] = 0
                else:
                    arena[i-8] = int(decode_list[i])
    print(ours, enemy, arena)
    radius = 40 #hardcoded value
    if ours[1]!= 0:
        print("move forward")
        payload_dict = {"cw": True, "move": True}
        payload_json = json.dumps(payload_dict)
        client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)
    else:
        print("dont move")
        payload_dict = {"cw": True, "move": False}
        payload_json = json.dumps(payload_dict)
        client.publish('raspberry/new', payload=payload_json, qos = 0, retain=False)






