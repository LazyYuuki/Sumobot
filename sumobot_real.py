from math import sqrt
import random
import numpy as np
from math import tan
from paho.mqtt import client as mqtt_client

broker = ''
port = 1883
topic = "" # fill in the topci
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = ''
# password = ''

#mqtt will allow us to send the movement data to the robot
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

class Sumobot():

    def __init__(self):

        self.done = False
        self.reward = 0
        self.enemy_reward = 0
        self.hit, self.miss = 0, 0
        
        #store defaults from the openmv such as arena and origin, fps
        #depending on the fps from openmv set the delay in arduino, and after each movement
        #execution, the command variable in arduino should reset to stop

        # Score
        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('black')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 100)
        self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))

        # -------------------- Keyboard control ----------------------

#         self.win.listen()
#         self.win.onkey(self.sumobot_right, 'Right')
#         self.win.onkey(self.sumobot_left, 'Left')
#         self.win.onkey(self.sumobot_up, 'Up')
#         self.win.onkey(self.sumobot_down, 'Down')

    #for each frame of data that comes in, run this function?
    #when we chagne resolution, the pixel count changes, so stick to a standard one.        
    def run_frame(self):        

        # Sumobot Arena contact

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
            self.sumobot.goto(0, -32)
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

    # ------------------------ AI control ------------------------

    # 0 do nothing
    # 1 move left
    # 2 move right
    # 3 move up
    # 4 move down
    # 5 top right
    # 6 top left
    # 7 bottom right
    # 8 bottom left

    def reset(self):

        self.sumobot.goto(0, -32)

        return [self.sumobot.xcor(), self.sumobot.ycor()] # maybe add enemy coordinates too

    def step(self, action):

        self.reward = 0
        self.done = 0
        angle = self.sumobot.towards(self.enemy.xcor(), self.enemy.ycor())
        arena_angle = self.sumobot.towards(0, 0)

        
        # 0 do nothing
        if action == 0:
            if sqrt(pow((self.enemy.xcor()-self.sumobot.xcor()), 2) + pow((self.enemy.ycor()-self.sumobot.ycor()), 2)) > 20:
                self.reward += 1000
            else:
                self.reward -= 1000
            self.sumobot_stop()
#             if sqrt(pow((self.enemy.xcor()-self.sumobot.xcor()), 2) + pow((self.enemy.ycor()-self.sumobot.ycor()), 2)) > 300:
#                 self.reward += 200
#             else:
#                 self.reward -= 100

        # 1 move left
        if action == 1:
            #close to the enemy
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
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
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                # robot in first and fourth quadrants edges
                if 135 < arena_angle < 225:
                    self.reward += 4000
                # robot in second and third quadrant edges
                elif arena_angle < 90 or arena_angle > 270:
                    self.reward -= 5000
            # rewarding unjustified movement
#             self.reward += 60
            self.sumobot_left()

        # 2 move right           
        if action == 2:
            #close to the enemy
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
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
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                # robot in left side edges
                if arena_angle < 45 or arena_angle > 315:
                    self.reward += 4000
                # robot in right side edges
                elif 135 < arena_angle < 225:
                    self.reward -= 5000
            # rewarding unjustified movement
#             self.reward += 60
            self.sumobot_right()

        # 3 move up   
        if action == 3:
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
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
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:  
                #robot at the bottom of the arena
                if (arena_angle < 45 or 135 < angle < 180):
                    self.reward += 1000
                elif (arena_angle < 180):
                    self.reward -= 2000
            # rewarding unjustified movement
#             self.reward += 60
            self.sumobot_up()
                
         # 4 move down
        if action == 4:
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10:
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
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
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:   
                # robot at the top of the arena
                if (225 < arena_angle < 315):
                    self.reward += 1000
                # robot at the bottom of the arena
                elif (45 < arena_angle < 135):
                    self.reward -= 2000
            # rewarding unjustified movement
#             self.reward += 60
            self.sumobot_down()
                
        # 5 top right      
        if action == 5:
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10: 
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                    if (90 < angle < 135 and 90 < arena_angle < 135) or ( angle > 270 and arena_angle > 315):
                        self.reward += 2000
                    elif (angle > 315 and arena_agle < 45) or (90 < angle < 180 and 45 < arena_angle < 90):
                        self.reward += 2000
                    elif (135 < arena_angle < 315):
                        self.reward -= 5000
                else: 
                    if(135 < angle < 315):
                        self.reward += 1000
                    else: 
                        self.reward -= 2000
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                if (135 < arena_angle < 315):
                    self.reward -= 5000
                else:
                    self.reward +=2000
            else:
#                 self.reward += 60
                self.sumobot_top_right()
                
        # 6 top left 
        if action == 6:
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10: 
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                    if((angle < 45 or angle > 315) and 45 < arena_angle < 90) or (225 < angle < 270 and 225 < arena_angle < 270):
                        self.reward += 2000
                    elif (180 < angle < 270 and 135 < arena_angle < 180) or (angle < 90 and 90 < arena_angle < 135):
                        self.reward += 2000
                    elif (arena_angle < 45 or arena_angle < 225):
                        self.reward -= 5000
                else:
                    if(angle < 45 or angle > 225):
                        self.reward += 1000
                    else:
                        self.reward -= 1000
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                if (45 < arena_angle < 225):
                    self.reward +=1000
                else:
                    self.reward -= 1000
            else:
#                 self.reward += 60
                self.sumobot_top_left()

        # 7 bottom right
        if action == 7:
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10: 
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                    if(45 < angle < 90 and arena_angle < 45) or (90 < angle < 180 and 225 < arena_angle < 270):
                        self.reward += 2000
                    elif(180 < angle < 270 and 270 < arena_angle < 315) or (angle < 90 and arena_angle > 315):
                        self.reward += 2000
                    elif (45 < arena_angle < 225):
                        self.reward -= 5000
                else:
                    if(45 < angle < 225):
                        self.reward += 1000
                    else:
                        self.reward -= 1000
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                if(45 < arena_angle < 225):
                    self.reward -= 2000
                else:
                    self.reward += 2000
            else:
#                 self.reward += 60
                self.sumobot_bottom_right()
        
        # 8 bottom left   
        if action == 8:
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10: 
                # close to the edge of the arena
                if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                    if((angle < 45 or angle > 315) and 270 < arena_angle < 315) or (90 < angle < 180 and 135 < arena_angle < 180):
                        self.reward += 2000
                    elif (angle < 270 and 225 < arena_angle < 270) or (90 < angle < 180 and 180 < arena_angle < 225):
                        self.reward += 2000
                    elif (arena_angle > 315 or arena_angle < 135):
                        self.reward -= 5000
                else:
                    if(angle > 315 or angle < 135):
                        self.reward += 2000
                    else:
                        self.reward -= 2000
            elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
                if(135 < arena_angle < 315):
                    self.reward += 1000
                else:
                    self.reward -= 1000
            else:
#                 self.reward += 60
                self.sumobot_bottom_left()

        self.run_frame()

        state = [self.sumobot.xcor(), self.sumobot.ycor()] # 2
        return self.reward, state, self.done
    


# ------------------------ Human control ------------------------
#
# env = Sumobot()

# while True:
#      env.run_frame()