import math 
from math import sqrt
import paho.mqtt.client as mqtt
import time, json, serial
import numpy as np
import random

ser=serial.Serial('/dev/ttyACM0',115200)
mqtt_username = "sumobot"
mqtt_password = "sumobot"
robot_topic = "raspberry/bot"


client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print("Connected")
    
movement = ["stop", "left", "right", "forward", 
	"backward", "upright", "downleft", 
"downright", "upleft", "clockwise", "anticlockwise"]
imu_angle = 0
def on_message(client, userdata, message):
    global imu_angle
    imu_angle = message.payload.decode("utf-8")
    #print(imu_angle)

def move_publish(tni):
    #print(movement[tni])
    client.loop_start()
    payload_dict = {"move": str(tni)}
    payload_dictjson = json.dumps(payload_dict)
    client.publish(robot_topic, payload=payload_dictjson, qos = 0, retain=False) # comes in the step command
    client.loop_stop()

client.on_connect = on_connect
client.connect("raspberrypi", 1883, 60)
client.on_message = on_message
client.subscribe("raspberry/imu")

decode_list = [0, 0, 0, 0, 0, 0, 0] #7 robotx, roboty, enemyx, enemyy, arena_radius, fps, imu

# calculate where enemy is located with respect to the sumobot    
def calculate_angle(robot_x, robot_y, enemy_x, enemy_y): #(x1,y1,x2,y2)
    myradians = math.atan2(enemy_y-robot_y, enemy_x-robot_x) # theta = tan^-1(dy/dx)
    mydegrees = math.degrees(myradians)
    if(enemy_x > robot_x and enemy_y > robot_y):
        return mydegrees
    elif(enemy_x < robot_x and enemy_y > robot_y):
        return mydegrees
    elif(enemy_x < robot_x and enemy_y < robot_y):
        return 360 + mydegrees
    elif(enemy_x > robot_x and enemy_y < robot_y):
        return 360 + mydegrees
    else:
        return 0
    
# calculate where enemy is located with respect to the arena center
def calculate_arena_angle(robot_x, robot_y):
    myradians = math.atan2(robot_y, robot_x)
    mydegrees = math.degrees(myradians)
    if(robot_x > 0 and robot_y > 0):
        return 180 + mydegrees
    elif(robot_x < 0 and robot_y > 0):
        return 180 + mydegrees
    elif(robot_x < 0 and robot_y < 0):
        return 180 + mydegrees
    elif(robot_x > 0 and robot_y < 0):
        return 180 + mydegrees
    else:
        return 0
    

while True:
    #client.loop()
    #client.loop_start()
    #move_publish(3)
    #time.sleep(0.1)
    
    readedText = ser.readline()
    decode = readedText.decode('UTF-8')
    decode = decode.replace("\r\n", "")
    temp_list = decode.split(',')
    if (len(temp_list) < 6):
        pass
    else:
        decode_list = [int(i) for i in temp_list]
        decode_list.append(imu_angle)

    # calculate the angle and arena_angle
    angle = 0
    arena_angle = 0
    # print(decode_list)
    angle = calculate_angle(decode_list[0], decode_list[1], decode_list[2], decode_list[3])
    arena_angle = calculate_arena_angle(decode_list[0], decode_list[1])
#     print(angle, arena_angle)
    #print(sqrt(pow((decode_list[2]-decode_list[0]), 2) + pow((decode_list[3]-decode_list[1]), 2)))
    #print(sqrt(pow((decode_list[2]-decode_list[0]), 2) + pow((decode_list[3]-decode_list[1]), 2)) < 40)
    #print(sqrt(pow(decode_list[0], 2) + pow(decode_list[1], 2)))
        
#                 
    #just close to the edge
    print(arena_angle)


