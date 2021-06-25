import math 
from math import sqrt
import paho.mqtt.client as mqtt
import time, json, serial
import numpy as np

ser=serial.Serial('/dev/ttyACM2',115200)
mqtt_username = "sumobot"
mqtt_password = "sumobot"
robot_topic = "raspberry/bot"


client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)
def on_connect(client, userdata, flags, rc):
    print("Connected")
    
movement = ["do nothing", "left", "right", "up", "down", "diagonalDownLeft", "diagonalUpRight", "diagonalUpLeft", "diagonalDownRight", "turnClockwise", "turnAntiClockwise"]
imu_angle = 0
def on_message(client, userdata, message):
    global imu_angle
    imu_angle = message.payload.decode("utf-8")
    #print(imu_angle)

def move_publish(tni):
    print(movement[tni])
    payload_dict = {"move": str(tni)}
    payload_json = json.dumps(payload_dict)
    client.publish(robot_topic, payload=payload_json, qos = 0, retain=False) # comes in the step command

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
        return 180 - mydegrees
    elif(enemy_x < robot_x and enemy_y < robot_y):
        return 180 + mydegrees
    elif(enemy_x > robot_x and enemy_y < robot_y):
        return 360 + mydegrees
    
# calculate where enemy is located with respect to the arena center
def calculate_arena_angle(robot_x, robot_y):
    myradians = math.atan2(robot_y, robot_x)
    mydegrees = math.degrees(myradians)
    if(robot_x > 0 and robot_y > 0):
        return mydegrees
    elif(robot_x < 0 and robot_y > 0):
        return 180 - mydegrees
    elif(robot_x < 0 and robot_y < 0):
        return 180 + mydegrees
    elif(robot_x > 0 and robot_y < 0):
        return 360 + mydegrees

while True:
    client.loop()
    #move_publish(3)
    
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
    #print(decode_list)
    
    angle = calculate_angle(decode_list[0], decode_list[1], decode_list[2], decode_list[3])
    arena_angle = calculate_arena_angle(decode_list[0], decode_list[1])
    #print(angle, arena_angle)
    
    #stop condition
    if sqrt(pow((decode_list[2]-decode_list[0]), 2) + pow((decode_list[3]-decode_list[1]), 2)) > 65:
        move_publish(0)

    #move condition
    elif sqrt(pow((decode_list[2]-decode_list[0]), 2) + pow((decode_list[3]-decode_list[1]), 2)) < 10:
        # close to the edge of the arena
        if sqrt(pow(decode_list[0], 2) + pow(decode_list[1], 2)) > 32:
            
            if (type(angle) == type(None)):
                angle = 90
            if(type(arena_angle) == type(None)):
                arena_angle = 90
            # enemy is in second or third quadrant respect to robot and robot is at the right of the arena
            if (225 < angle < 270 and 135 < arena_angle < 225) or (90 < angle < 135 and 135 < arena_angle < 225):
                move_publish(1)
                
            elif (45 < angle < 90 and 45 < arena_angle < 135) or (angle > 315 and 225 < arena_angle < 315):
                move_publish(1)
                

            # enemy is in second and third quadrant respect to robot and robot is at the bottom and top of the arena
            elif (90 < angle < 135 and 45 < angle < 90) or (225 < angle < 270 and 270 < arena_angle < 315):
                move_publish(2)
                
            # enemy is in first and fourth quadrant respect to robot and robot is at the bottom and top of the arena
            elif (45 < angle < 90 and 90 < angle < 135) or (270 < angle < 315 and 270 < arena_angle < 315):
                move_publish(2)
                
            # enemy is in first and fourth quadrant respect to robot and robot is at the left of the arena
            elif (270 < angle < 315 and 45 < arena_angle < 90) or (45 < angle < 90 and 270 < arena_angle < 315):
                move_publish(2)
                
            # enemy in fourth and third quadrant and robot in the left and right side of the arena
            elif (angle < 315 and arena_angle < 45) or (180 < angle < 225 and 135 < arena_angle < 180):
                move_publish(3)
                
            # enemy on the first and second quadrant with respect to robot and robot at the bottom of the arena
            elif (angle < 45 and 45 < arena_angle < 135) or (135 < angle < 180 and 45 < arena_angle < 135):
                move_publish(3)
                
            # enemy on the left and right of the robot and robot at the top of the arena
            elif (180 < angle < 225 and 225 < arena_angle < 270) or (angle < 315 and 270 < arena_angle < 315):
                move_publish(4)
                
            # enemy on the right and left of the robot and the robot on the left and right of the arena
            elif (45 < angle < 90 and arena_angle < 315) or (90 < angle < 135 and 180 < arena_angle < 225):
                move_publish(4)
                
            elif (90 < angle < 135 and 90 < arena_angle < 135) or ( angle > 270 and arena_angle > 315):
                move_publish(5)
                
            elif (angle > 315 and arena_angle < 45) or (90 < angle < 180 and 45 < arena_angle < 90):
                move_publish(5)
                
            elif((angle < 45 or angle > 315) and 45 < arena_angle < 90) or (225 < angle < 270 and 225 < arena_angle < 270):
                move_publish(6)
                
            elif (180 < angle < 270 and 135 < arena_angle < 180) or (angle < 90 and 90 < arena_angle < 135):
                move_publish(6)
                
            elif(45 < angle < 90 and arena_angle < 45) or (90 < angle < 180 and 225 < arena_angle < 270):
                move_publish(7)
                
            elif(180 < angle < 270 and 270 < arena_angle < 315) or (angle < 90 and arena_angle > 315):
                move_publish(7)
                
            elif((angle < 45 or angle > 315) and 270 < arena_angle < 315) or (90 < angle < 180 and 135 < arena_angle < 180):
                move_publish(8)
                
            elif (angle < 270 and 225 < arena_angle < 270) or (90 < angle < 180 and 180 < arena_angle < 225):
                move_publish(8)
                
        #case of not being close to the arena
        else:
            # enemy in first and fourth quadrants
            if angle < 90 or angle > 270:
                move_publish(1)
                
            if 90 < angle < 270:
                move_publish(2)
                
            if(180 < angle):
                move_publish(3)
                
            if(45 < angle < 135):
                move_publish(4)
                
            if(135 < angle < 315):
                move_publish(5)
                
            if(angle < 45 or angle > 225):
                move_publish(6)
                
            if(45 < arena_angle < 225):
                move_publish(7)
                
            if(angle > 315 or angle < 135):
                move_publish(8)
                
    #just close to the edge
    elif sqrt(pow(decode_list[0], 2) + pow(decode_list[1], 2)) > 32:
        # robot in first and fourth quadrants edges
        if 135 < arena_angle < 225:
            move_publish(1)       
            
        # robot in left side edges
        if arena_angle < 45 or arena_angle > 315:
            move_publish(2)
            
        #robot at the bottom of the arena
        if (arena_angle < 45 or 135 < angle < 180):
            move_publish(3)
            
        # robot at the top of the arena
        if (225 < arena_angle < 315):
            move_publish(4)
            
        if (135 < arena_angle < 315):
            move_publish(5)
            
        if (45 < arena_angle < 225):
            move_publish(6)
            
        if(45 < arena_angle < 225):
            move_publish(7)
            
        if(135 < arena_angle < 315):
            move_publish(8)
        else:
            move_publish(1)
    
                


