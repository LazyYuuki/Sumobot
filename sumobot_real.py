from math import sqrt
import random
import numpy as np
from math import tan
import json 
import paho.mqtt.client as mqtt

broker = '192.168.1.13'
topic = "raspberry/new" 
robot_topic = "raspberry/bot"
mqtt_username = "sumobot"
mqtt_password = "sumobot"
movement = ["do nothing", "left", "right", "up", "down", "top right", "top left", "bottom right", "bottom left"]

state = [0, 0, 0, 0, 0, 0] # robotx, roboty, enemyx, enemyy, fps, arena_radius, imu

def on_message(client, userdata, message):
    arr = message.payload.decode("utf-8").split(", ")
    for i in range(0, len(arr)):
        state[i] = int(arr[i]) 
        
def on_connect(client, userdata, flags, rc):
    print("Connected")


class Sumobot():

    def __init__(self):

        self.done = False
        self.reward = 0
        self.enemy_reward = 0
        self.hit, self.miss = 0, 0

        #mqtt initializing
        self.client = mqtt.Client()
        self.client.username_pw_set(mqtt_username, mqtt_password)
        self.client.on_connect = on_connect
        self.client.on_message = on_message 
        self.client.connect(broker, 1883, 60)
        self.client.subscribe(topic) # subscribing to the information from raspberry
        self.client.loop_start()


        # Score
        self.score = 0
        self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))

#         # -------------------- Keyboard control ----------------------

# #         self.win.listen()
# #         self.win.onkey(self.sumobot_right, 'Right')
# #         self.win.onkey(self.sumobot_left, 'Left')
# #         self.win.onkey(self.sumobot_up, 'Up')
# #         self.win.onkey(self.sumobot_down, 'Down')

    #for each frame of data that comes in, run this function?
    #when we change resolution, the pixel count changes, so stick to a standard one.        
    def run_frame(self):        
        
        # store defaults from the openmv such as arena and origin, fps
        # depending on the fps from openmv set the delay in arduino, and after each movement
        # execution, the command variable in arduino should reset to stop
        #subscribe to get the intial values.
        self.fps = state[4]
        self.arena_radius = [5]
        if(self.fps):
            self.delay = 1000/self.fps

        
        # Sumobot Arena contact
        if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:
            self.reset()
            self.miss += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward -= 1000
#             self.enemy_reward += 1000
            self.done = True
        else:
            self.reward += 1000
#             self.enemy_reward -= 400            

#     # ------------------------ AI control ------------------------

#     # 0 do nothing
#     # 1 move left
#     # 2 move right
#     # 3 move up
#     # 4 move down


    def reset(self):

        #do a proper reset funcion

        return state # maybe add enemy coordinates too

    def step(self, action):

        self.reward = 0
        self.done = 0
        self.client.loop_start()
        # calculate the angle and arena_angle
        
        # 0 do nothing
        if action == 0:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) > 20:
                self.reward += 1000
            else:
                self.reward -= 1000
            
            payload_dict = {"move": str(0)}
            payload_json = json.dumps(payload_dict)
            self.client.publish(robot_topic, payload=payload_json, qos = 0, retain=False) # comes in the step command
#             if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) > 300:
#                 self.reward += 200
#             else:
#                 self.reward -= 100

        # 1 move left
        if action == 1:
            #close to the enemy
            if sqrt(pow(state[0], 2) + pow(state[3] - state[1], 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:
                    # enemy is in second or third quadrant respect to robot and robot is at the right of the arena
                    if (225 < angle < 270 and 135 < arena_angle < 225) or (90 < angle < 135 and 135 < arena_angle < 225):
                        self.reward += 2000
                    # enemy is in first or fourth quadrant respect to robot and robot is at the bottom and top of the arena
                    elif (45 < angle < 90 and 45 < arena_angle < 135) or (angle > 315 and 225 < arena_angle < 315):
                        self.reward += 1000
                    # enemy is in second or third quadrant respect to robot and robot is at the bottom and top of the arena
                    elif (90 < angle < 135 and 45 < arena_angle < 135) or (225 < angle < 270 and 225 < arena_angle < 315):
                        self.reward -= 1000
                    # robot in second and third quadrant edges and enemy presumably on the right of the robot
                    elif arena_angle < 90 or arena_angle > 270:
                        self.reward -= 5000
                #case of not being close to the arena
                else:
                    # enemy in first and fourth quadrants
                    if angle < 90 or angle > 270:
                        self.reward += 1000
                    # enemy in second and thrid quadrants
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:
                # robot in first and fourth quadrants edges
                if 135 < arena_angle < 225:
                    self.reward += 4000
                # robot in second and third quadrant edges
                elif arena_angle < 90 or arena_angle > 270:
                    self.reward -= 5000
            # rewarding unjustified movement
#             self.reward += 60
            payload_dict = {"move": str(1)}
            payload_json = json.dumps(payload_dict)
            self.client.publish(robot_topic, payload=payload_json, qos = 0, retain=False) # comes in the action command

        # 2 move right           
        if action == 2:
            #close to the enemy
            if sqrt(pow(state[0], 2) + pow(state[3] - state[1], 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:
                    # enemy is in second and third quadrant respect to robot and robot is at the bottom and top of the arena
                    if (90 < angle < 135 and 45 < angle < 90) or (225 < angle < 270 and 270 < arena_angle < 315):
                        self.reward += 2000
                    # enemy is in first and fourth quadrant respect to robot and robot is at the bottom and top of the arena
                    elif (45 < angle < 90 and 90 < angle < 135) or (270 < angle < 315 and 270 < arena_angle < 315):
                        self.reward += 1000
                    # enemy is in first and fourth quadrant respect to robot and robot is at the left of the arena
                    elif (270 < angle < 315 and 45 < arena_angle < 90) or (45 < angle < 90 and 270 < arena_angle < 315):
                        self.reward += 1000
                    # robot in first and fourth quadrant edges and enemy presumably on the left side
                    elif 90 < arena_angle < 270:
                        self.reward -= 5000
                #case of not being close to the arena
                else:
                    # enemy in second and third quadrants
                    if 90 < angle < 270:
                        self.reward += 1000
                    # enemy in second and thrid quadrants
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:
                # robot in left side edges
                if arena_angle < 45 or arena_angle > 315:
                    self.reward += 4000
                # robot in right side edges
                elif 135 < arena_angle < 225:
                    self.reward -= 5000
            # rewarding unjustified movement
#             self.reward += 60
            payload_dict = {"move": str(2)}
            payload_json = json.dumps(payload_dict)
            self.client.publish(robot_topic, payload=payload_json, qos = 0, retain=False) # comes in the action command

        # 3 move up   
        if action == 3:
            if sqrt(pow(state[0], 2) + pow(state[3] - state[1], 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:
                    # enemy in fourth and third quadrant and robot in the left and right side of the arena
                    if (angle < 315 and arena_angle < 45) or (180 < angle < 225 and 135 < arena_angle < 180):
                        self.reward += 2000
                    # enemy on the first and second quadrant with respect to robot and robot at the bottom of the arena
                    elif (angle < 45 and 45 < arena_angle < 135) or (135 < angle < 180 and 45 < arena_angle < 135):
                        self.reward += 1000
                    # robot at the top of the arena
                    elif (arena_angle < 180):
                        self.reward -= 5000
                # case of not being close to the arena
                else:
                    #enemy below the robot
                    if(180 < angle):
                        self.reward += 1000
                    #enemy on top of the robot
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:  
                #robot at the bottom of the arena
                if (arena_angle < 45 or 135 < angle < 180):
                    self.reward += 1000
                elif (arena_angle < 180):
                    self.reward -= 2000
            # rewarding unjustified movement
#             self.reward += 60
            payload_dict = {"move": str(3)}
            payload_json = json.dumps(payload_dict)
            self.client.publish(robot_topic, payload=payload_json, qos = 0, retain=False) # comes in the action command
                
         # 4 move down
        if action == 4:
            if sqrt(pow(state[0], 2) + pow(state[3] - state[1], 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:
                    # enemy on the left and right of the robot and robot at the top of the arena
                    if (180 < angle < 225 and 225 < arena_angle < 270) or (angle < 315 and 270 < arena_angle < 315):
                        self.reward += 2000
                    # enemy on the right and left of the robot and the robot on the left and right of the arena
                    elif (45 < angle < 90 and arena_angle < 315) or (90 < angle < 135 and 180 < arena_angle < 225):
                        self.reward += 1000
                    # robot at the bottom of the arena
                    elif (45 < arena_angle < 135):
                        self.reward -= 5000
                # case of not being close to the arena
                else:
                    if(45 < angle < 135):
                        self.reward += 1000
                    elif(angle < 180):
                        self.reward -=2000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 32:   
                # robot at the top of the arena
                if (225 < arena_angle < 315):
                    self.reward += 1000
                # robot at the bottom of the arena
                elif (45 < arena_angle < 135):
                    self.reward -= 2000
            # rewarding unjustified movement
#             self.reward += 60
            payload_dict = {"move": str(4)}
            payload_json = json.dumps(payload_dict)
            self.client.publish(robot_topic, payload=payload_json, qos = 0, retain=False) # comes in the action command
                
        
        self.run_frame()

        return self.reward, state, self.done


# ------------------------ Human control ------------------------
#
# env = Sumobot()

# while True:
#      env.run_frame()