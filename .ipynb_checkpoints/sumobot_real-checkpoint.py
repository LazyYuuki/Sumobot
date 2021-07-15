########
# if enemy outside, stop the thing, reset
# sumobot should reset it's position to be trained from the said points
########
from CV.rpi.hardCode import move_publish
import math
from math import sqrt
import random
import numpy as np
from math import atan2, degrees
import json 
import paho.mqtt.client as mqtt

broker = '192.168.1.17'
topic = "raspberry/new" 
robot_topic = "raspberry/bot"
reset_topic = "raspberry/reset"
mqtt_username = "sumobot"
mqtt_password = "sumobot"
movement = ["do nothing", "left", "right", "up", "down", "diagonalDownLeft", "diagonalUpRight", "diagonalUpLeft", "diagonalDownRight", "turnClockwise", "turnAntiClockwise"]

state = [0, 0, 0, 0, 0, 0, 0] #7 robotx, roboty, enemyx, enemyy, arena_radius, fps, imu

def on_message(client, userdata, message):
    arr = message.payload.decode("utf-8").split(", ")
    # for different topics, use message.topic
    if(message.topic == 'raspberry/new'):
        for i in range(0, len(arr)):
            state[i] = int(arr[i]) 
        
def on_connect(client, userdata, flags, rc):
    print("Connected")
    
    
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
    
class Sumobot():

    def __init__(self):

        self.done = False # to end a learning epsiode
        self.reward = 0 #cumulative reward after an episode
        self.hit, self.miss = 0, 0

        #mqtt initializing
        self.client = mqtt.Client()
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.client.on_connect = on_connect
        self.client.on_message = on_message 
        self.client.connect(broker, 1883, 60)
        self.client.subscribe(topic) # subscribing to the information from raspberry
        self.client.loop_start()

    #for each frame of data that comes in, run this function
    #when we change resolution, the pixel count changes, so stick to a standard one.  
    def move_publish(self, tni):
        #print(movement[tni])
        self.client.loop_start()
        payload_dict = {"move": str(tni)}
        payload_dictjson = json.dumps(payload_dict)
        self.client.publish(robot_topic, payload=payload_dictjson, qos = 0, retain=False) # comes in the step command
        self.client.loop_stop()          

    def run_frame(self):        
        
        # store defaults from the openmv such as arena and origin, fps
        # depending on the fps from openmv set the delay in arduino, and after each movement
        # execution, the command variable in arduino should reset to stop
        #subscribe to get the intial values.
        self.arena_radius = state[4]
        self.fps = state[5] # can be moved to the constructor 
        if(self.fps):
            self.delay = 1000/self.fps
            
        # 1. Write reset function (in the works)
                    # - do the imu heading
                    # - do the x and y coordinate movement

        # Sumobot Arena contact
        if sqrt(pow(state[0], 2) + pow(state[1], 2)) > (self.arena_radius - 8):
            self.reset()
            self.miss += 1
            # self.score.clear()
            # self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward -= 10000
            self.done = True
        else:
            self.reward += 1000
            # self.enemy_reward -= 400 

        # Enemy Arena Contact
        if sqrt(pow(state[3], 2) + pow(state[4], 2)) > (self.arena_radius - 8):
            self.reset()
            self.reward += 4000
            self.done = True
        else:
            self.reward -= 10
            
        # Sumobot Enemy Contact
        if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 8:
            self.reward -= 3000
        # if not close to the enemy
        elif sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) > 10:
            self.reward += 1000

     # ------------------------ AI control ------------------------

     # 0 do nothing
     # 1 move left
     # 2 move right
     # 3 move up
     # 4 move down


    def reset(self):
        # nodemcu to go into reset mode
        self.move_publish(13)
        return state 

    def step(self, action):

        self.reward = 0
        self.done = 0
        self.client.loop_start()
        # calculate the angle and arena_angle
        angle = calculate_angle(state[0], state[1], state[2], state[3])
        arena_angle = calculate_arena_angle(state[0], state[1])
        
        # 0 do nothing
        if action == 0:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) > 30:
                self.reward += 1000
            else:
                self.reward -= 1000
            self.move_publish(0)
            

        # 1 move left
        elif action == 1:
            #close to the enemy
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                self.move_publish(1) 
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 3
                    if(0 < angle < 90 and 70 < arena_angle < 180):
                        print("here 1")
                        self.reward += 2000
                    # # enemy is in second or third quadrant respect to robot and robot is at the right of the arena
                    # #change this to move_right
                    # elif (225 < angle < 270 and 135 < arena_angle < 225) or (90 < angle < 135 and 135 < arena_angle < 225):
                    #     self.reward += 2000
                        
                    # # enemy is in first or fourth quadrant respect to robot and robot is at the bottom and top of the arena
                    # elif (45 < angle < 90 and 45 < arena_angle < 135) or (angle > 315 and 225 < arena_angle < 315):
                    #     self.reward += 1000
                        
                    # # enemy is in second or third quadrant respect to robot and robot is at the bottom and top of the arena
                    # elif (90 < angle < 135 and 45 < arena_angle < 135) or (225 < angle < 270 and 225 < arena_angle < 315):
                    #     self.reward -= 1000
                        
                    # # robot in second and third quadrant edges and enemy presumably on the right of the robot
                    # elif arena_angle < 90 or arena_angle > 270:
                    #     self.reward -= 5000
                        
                #case of not being close to the arena
                else:
                    # enemy in first and fourth quadrants
                    if angle < 90 or angle > 270:
                        print("here 12")
                        self.reward += 1000
                    # enemy in second and thrid quadrants
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                # robot in first and fourth quadrants edges
                if 135 < arena_angle < 225:
                    self.reward += 4000
                # # robot in second and third quadrant edges
                # elif arena_angle < 90 or arena_angle > 270:
                #     self.reward -= 5000
            self.move_publish(1)

            
        # 2 move right           
        elif action == 2:
            # close to the enemy
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 2
                    if (90 < angle < 180 and 0 < arena_angle < 110):
                        print('here 2')
                        self.reward += 2000
                    # # enemy is in second and third quadrant respect to robot and robot is at the bottom and top of the arena
                    # elif (90 < angle < 135 and 45 < arena_angle < 90) or (225 < angle < 270 and 270 < arena_angle < 315):
                    #     self.reward += 2000
                        
                    # # enemy is in first and fourth quadrant respect to robot and robot is at the bottom and top of the arena
                    # elif (45 < angle < 90 and 90 < arena_angle < 135) or (270 < angle < 315 and 270 < arena_angle < 315):
                    #     self.reward += 1000
                        
                    # # enemy is in first and fourth quadrant respect to robot and robot is at the left of the arena
                    # elif (270 < angle < 315 and 45 < arena_angle < 90) or (45 < angle < 90 and 270 < arena_angle < 315):
                    #     self.reward += 1000
                        
                    # # robot in first and fourth quadrant edges and enemy presumably on the left side
                    # elif 90 < arena_angle < 270:
                    #     self.reward -= 5000
                        
                #case of not being close to the arena
                else:
                    # enemy in second and third quadrants
                    if 90 < angle < 270:
                        self.reward += 1000
                    # enemy in second and thrid quadrants
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                # robot in left side edges
                if arena_angle < 45 or arena_angle > 315:
                    self.reward += 4000
                # # robot in right side edges
                # elif 135 < arena_angle < 225:
                #     self.reward -= 5000
            self.move_publish(2)
            

        # 3 move up   
        elif action == 3:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 5
                    if(90 < angle < 180 and 150 < arena_angle < 225):
                        print('here 3')
                        self.reward += 2000

                    # # enemy in fourth and third quadrant and robot in the left and right side of the arena
                    # elif (angle < 315 and arena_angle < 45) or (180 < angle < 225 and 135 < arena_angle < 180):
                    #     self.reward += 2000
                        
                    # # enemy on the first and second quadrant with respect to robot and robot at the bottom of the arena
                    # elif (angle < 45 and 45 < arena_angle < 135) or (135 < angle < 180 and 45 < arena_angle < 135):
                    #     self.reward += 1000
                        
                    # # robot at the top of the arena
                    # elif (arena_angle < 180):
                    #     self.reward -= 5000
                # case of not being close to the arena
                else:
                    #enemy below the robot
                    if(180 < angle):
                        print("here 32")
                        self.reward += 1000               
                    #enemy on top of the robot
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                #robot at the bottom of the arena
                if (225 < arena_angle < 315):
                    self.reward += 1000
                    
                # elif (arena_angle < 180):
                #     self.reward -= 2000             
            self.move_publish(3)
            
                
         # 4 move down
        elif action == 4:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 2
                    if (90 < angle < 180 and 0 < arena_angle < 110):
                        print('here 2')
                        self.reward += 2000

                    # # enemy on the left and right of the robot and robot at the top of the arena
                    # elif (180 < angle < 225 and 225 < arena_angle < 270) or (angle > 315 and 270 < arena_angle < 315):
                    #     self.reward += 2000
                        
                    # # enemy on the right and left of the robot and the robot on the left and right of the arena
                    # elif (45 < angle < 90 and arena_angle < 315) or (90 < angle < 135 and 180 < arena_angle < 225):
                    #     self.reward += 1000
                        
                    # # robot at the bottom of the arena
                    # elif (45 < arena_angle < 135):
                    #     self.reward -= 5000
                # case of not being close to the arena
                else:
                    if(45 < angle < 135):
                        print("here 42")
                        self.reward += 1000
                        
                    # elif(angle < 180):
                    #     self.reward -=2000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                # robot at the top of the arena
                if (45 < arena_angle < 135):
                    self.reward += 1000
                # # robot at the bottom of the arena
                # elif (225 < arena_angle < 315):
                #     self.reward -= 2000            
            self.move_publish(4)
            
        
        elif action == 5:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 6
                    if(180 < angle < 270 and 135 < arena_angle < 210):
                        print("here 5")
                        self.reward += 2000

                    # elif (90 < angle < 135 and 90 < arena_angle < 135) or ( angle > 270 and arena_angle > 315):
                    #     self.reward += 2000
                        
                    # elif (angle > 315 and arena_angle < 45) or (90 < angle < 180 and 45 < arena_angle < 90):
                    #     self.reward += 2000
                        
                    # elif (135 < arena_angle < 315):
                    #     self.reward -= 5000
                else: 
                    if(135 < angle < 315):
                        print("here 52")
                        self.reward += 1000    
                    else: 
                        self.reward -= 2000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                if (135 < arena_angle < 180):
                    self.reward +=2000
                else:
                    self.reward -= 5000
            self.move_publish(5)
            
                

        elif action == 6:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 9
                    if(180 < angle < 270 and arena_angle > 250):
                        print("here 6")
                        self.reward += 2000

                    # elif((angle < 45 or angle > 315) and 45 < arena_angle < 90) or (225 < angle < 270 and 225 < arena_angle < 270):
                    #     self.reward += 2000
                        
                    # elif (180 < angle < 270 and 135 < arena_angle < 180) or (angle < 90 and 90 < arena_angle < 135):
                    #     self.reward += 2000
                        
                    # elif (arena_angle < 45 or arena_angle < 225):
                    #     self.reward -= 5000
                else:
                    if(angle < 45 or angle > 225):
                        self.reward += 1000
                    else:
                        self.reward -= 1000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                if (315 < arena_angle < 360):
                    self.reward +=1000
                else:
                    self.reward -= 1000        
            self.move_publish(6)
            

        elif action == 7:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 8
                    if(270 < angle < 360 and 180 < arena_angle < 290):
                        print("here 7")
                        move_publish(7)
                    # elif(45 < angle < 90 and arena_angle < 45) or (90 < angle < 180 and 225 < arena_angle < 270):
                    #     self.reward += 2000
                        
                    # elif(180 < angle < 270 and 270 < arena_angle < 315) or (angle < 90 and arena_angle > 315):
                    #     self.reward += 2000
                        
                    # elif (45 < arena_angle < 225):
                    #     self.reward -= 5000
                else:
                    if(45 < angle < 225):
                        self.reward += 1000
                    else:
                        self.reward -= 1000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                if(180 < arena_angle < 225):
                    self.reward -= 2000
                else:
                    self.reward += 2000
            self.move_publish(7)
            

        elif action == 8:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 11
                    if(270 < angle < 360 and (arena_angle < 90 or arena_angle > 340)):
                        print("here 8")
                    # elif((angle < 45 or angle > 315) and 270 < arena_angle < 315) or (90 < angle < 180 and 135 < arena_angle < 180):
                    #     self.reward += 2000
                        
                    # elif (angle < 270 and 225 < arena_angle < 270) or (90 < angle < 180 and 180 < arena_angle < 225):
                    #     self.reward += 2000
                        
                    # elif (arena_angle > 315 or arena_angle < 135):
                    #     self.reward -= 5000
                else:
                    if(angle > 315 or angle < 135):
                        print("here 82")
                        self.reward += 2000
                    else:
                        self.reward -= 2000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                if(0 < arena_angle < 45):
                    self.reward += 1000
                    
                else:
                    self.reward -= 1000
            self.move_publish(8)
            

        # all the  statements will come to this part
        self.run_frame()

        return self.reward, state, self.done


# ------------------------ Human control ------------------------
#
# env = Sumobot()

# while True:
#      env.run_frame()


