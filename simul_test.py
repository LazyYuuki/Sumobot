import turtle as t
import math
from math import sqrt
import random
import numpy as np
import cmath
import time


##
# do the axis match? since, we train it beased on testing, i think they do?
# looks like arena angle is shited by 180 deg and it's direction of rotation flipped
# "angle" between enemy and sumobot, seems to take as with respect to enemy as center 

class Sumobot():

    def __init__(self):
        self.done = False
        self.reward = 0
        self.radius = -36
        self.radius_delta = 8
        self.angle = 0
        self.angle_delta = 30        
        self.arena_radius = 44
        self.speed = 0

        
        t.clearscreen()
        t.pu()
        t.setpos(-self.arena_radius,0)
        t.right(90)
        t.pd()
        t.circle(self.arena_radius)
        t.pu()
        
        # Sumobot
        self.sumobot = t.Turtle()
        self.sumobot.speed(0)
        self.sumobot.shape('square')
        self.sumobot.shapesize(stretch_wid=0.2, stretch_len=0.2)
        self.sumobot.color('blue')
        self.sumobot.pu()
        self.sumobot.goto(random.randint(-30,30), random.randint(-30,30))
        self.sumobot.dx = 0
        self.sumobot.dy = 0
        
        # Enemy
        self.enemy = t.Turtle()
        self.enemy.speed(0)
        self.enemy.shapesize(stretch_wid=0.2, stretch_len=0.2)
        self.enemy.shape('square')
        self.enemy.color('red')
        self.enemy.pu()
        self.enemy.goto(random.randint(-30,30), random.randint(-30,30))
        self.enemy.dx = 0
        self.enemy.dy = 0
        #self.enemy.shapesize(stretch_wid=4, stretch_len=4)


    # Sumobot movement

    def sumobot_right(self):

        self.sumobot.dx = self.speed
        self.sumobot.dy = 0

    def sumobot_left(self):

        self.sumobot.dx = -self.speed
        self.sumobot.dy = 0
            
    def sumobot_up(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = self.speed
    
    def sumobot_down(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = -self.speed
    
    def sumobot_stop(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = 0
        
    def sumobot_top_right(self):
        self.sumobot.dx = self.speed
        self.sumobot.dy = self.speed
        
    def sumobot_top_left(self):
        self.sumobot.dx = -self.speed
        self.sumobot.dy = self.speed
        
    def sumobot_bottom_right(self):
        self.sumobot.dx = self.speed
        self.sumobot.dy = -self.speed
        
    def sumobot_bottom_left(self):
        self.sumobot.dx = -self.speed
        self.sumobot.dy = -self.speed

        

    def red_dot(self):
        t.pd()
        t.dot('red')
        t.pu()
        
    def blue_dot(self):
        t.pd()
        t.dot('blue')
        t.pu()
        
    def sumobot_spiral(self, angle, radius):
        x = math.sqrt((radius**2)/(1 + (math.tan(math.radians(angle)))**2))
        y = x * math.tan(math.radians(angle))
        if 0 <= angle <= 90:
            self.sumobot.goto(-x,-y)
        elif 90 < angle <= 180:
            self.sumobot.goto(x,y)
        elif 180 < angle <= 270:
            self.sumobot.goto(x,y)
        elif 270 < angle < 360:
            self.sumobot.goto(-x,-y)
        #self.red_dot()
   
    def run_frame(self):
    
        angle = math.radians(self.enemy.towards(self.sumobot.xcor(), self.sumobot.ycor()))
        distance = math.dist([self.sumobot.xcor(), self.sumobot.ycor()], [self.enemy.xcor(), self.enemy.ycor()])
        
        if distance == 0:
            distance = 1
        
        dy = distance * math.sin(angle)
        dx = distance * math.cos(angle)
        
        scale = (random.randint(1, 3))/sqrt(pow(dx,2) + pow(dy,2))
        
        self.enemy.dx = dx * scale
        self.enemy.dy = dy * scale
        
        # print(angle, distance, self.enemy.dx, self.enemy.dy)
        
        self.enemy.setx(self.enemy.xcor() + self.enemy.dx)
        self.enemy.sety(self.enemy.ycor() + self.enemy.dy)
            
        # Sumobot Arena contact
<<<<<<< HEAD

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 36:
            # so these two "goto"s should take the values of the particular case we are in
            self.sumobot.goto(self.state[0], self.state[1])
            self.reward -= 8000
            self.done = False # maybe remove this, for one of the training
=======
        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 37:
            # so these two "goto"s should take the values of the particular case we are in
            self.reward -= 9
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
        else:
            if sqrt(pow(self.enemy.xcor() - self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 17:
                # so these two "goto"s should take the values of the particular case we are in
                self.reward -= 3
            else:
                self.reward += 3
            
        # stay as far as possible from enemy    
<<<<<<< HEAD
        if sqrt(pow((self.enemy.xcor()-self.sumobot.xcor()), 2) + pow((self.enemy.ycor()-self.sumobot.ycor()), 2)) > 45:
            self.reward += 1500
        elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10:
            self.reward -= 5000
        else:
            self.reward += 3000
            
        # Enemy Sumobot collision

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 6:
            self.reward -= 1000
=======
        # if  sqrt(pow(self.enemy.xcor() - self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 20:
        #    self.reward -= 100
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            
    def reset(self, episode_coords):
        # so these two "goto"s should take the values of the particular case we are in
        # so i think they'll go inside the giant for loop
        self.sumobot.goto(episode_coords[0][0], episode_coords[0][1])
        self.enemy.goto(episode_coords[1][0], episode_coords[1][1])
        return [self.sumobot.xcor(), self.sumobot.ycor(), self.enemy.xcor(), self.enemy.ycor()] # maybe add enemy coordinates too
        
        
    def step(self, action):
        self.reward = 0
        self.done = 0
        angle = self.enemy.towards(self.sumobot.xcor(), self.sumobot.ycor())
        #need to transform the arena angle
        arena_angle = self.sumobot.towards(0, 0)
        
        self.speed = random.randint(1, 3)
        
        # 0 do nothing
        if action == 0:
<<<<<<< HEAD
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) > 34:
                self.reward += 1000
            else:
                self.reward -= 1000
=======
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            self.sumobot_stop()
        
        # 1 move left
        elif action == 1:
<<<<<<< HEAD
            #close to the enemy
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 20 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                    #case 3
                    if(0 < angle < 90 and 70 < arena_angle < 180):
                        self.reward += 2000
                    elif (45 < angle < 90 and 45 < arena_angle < 135) or (angle > 315 and 225 < arena_angle < 315):
                        self.reward += 1000
                    # enemy is in second or third quadrant respect to robot and robot is at the bottom and top of the arena
                    elif (90 < angle < 135 and 45 < arena_angle < 135) or (225 < angle < 270 and 225 < arena_angle < 315):
                        self.reward -= 1000
                    elif (arena_angle < 90 or arena_angle > 270) and (angle < 90 or angle > 270):
                        self.reward -= 7000
                #case of not being close to the arena
                else:
                    # enemy in first and fourth quadrants
                    if angle < 90 or angle > 270:
                        self.reward += 1000
                    # enemy in second and thrid quadrants
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 35:
                # robot in first and fourth quadrants edges
                if 135 < arena_angle < 225:
                    self.reward += 4000
                # robot in second and third quadrant edges
                elif arena_angle < 90 or arena_angle > 270:
                    self.reward -= 7000
=======
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            self.sumobot_left()
            self.reward -= 0.1
        
        # 2 move right   
        elif action == 2:
<<<<<<< HEAD
            # close to the enemy
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 18 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                    #case 2
                    if (90 < angle < 180 and 0 < arena_angle < 110):
                        self.reward += 2000
                    elif (90 < angle < 135 and 45 < arena_angle < 90) or (225 < angle < 270 and 270 < arena_angle < 315):
                        self.reward += 2000
                    elif (225 < angle < 270 and 135 < arena_angle < 225) or (90 < angle < 135 and 135 < arena_angle < 225):
                        self.reward += 2000
                #case of not being close to the arena
                else:
                    # enemy in second and third quadrants
                    if 90 < angle < 270:
                        self.reward += 1000
                    # enemy in second and thrid quadrants
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                # robot in left side edges
                if arena_angle < 45 or arena_angle > 315:
                    self.reward += 4000
                # # robot in right side edges
                elif 135 < arena_angle < 225:
                    self.reward -= 7000
=======
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            self.sumobot_right()
            self.reward -= 0.1
  
        # 3 move up  
        elif action == 3:
<<<<<<< HEAD
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 18 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                    #case 5
                    if(90 < angle < 180 and 170 < arena_angle < 270):
                        self.reward += 2000
                     # robot at the top of the arena
                    elif (arena_angle < 180):
                        self.reward -= 7000
                # case of not being close to the arena
                else:
                    #enemy below the robot
                    if(180 < angle):
                        self.reward += 1000               
                    #enemy on top of the robot
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                #robot at the bottom of the arena
                if (225 < arena_angle < 315):
                    self.reward += 1000
                elif (arena_angle < 180):
                    self.reward -= 2000         
=======
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            self.sumobot_up()
            self.reward -= 0.1
            
         # 4 move down
        elif action == 4:
<<<<<<< HEAD
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 18 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                    #case 2
                    if (90 < angle < 180 and 0 < arena_angle < 110):
                        self.reward += 2000
                    elif (angle > 315 and 270 < arena_angle < 315):
                        self.reward += 2000
                    elif (225 < arena_angle < 315):
                        self.reward -= 7000
                 # case of not being close to the arena
                else:
                    if(45 < angle < 135):
                        self.reward += 1000                        
                    elif(angle < 180):
                        self.reward -=2000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                # robot at the top of the arena
                if (45 < arena_angle < 135):
                    self.reward += 1000 
                # robot at the bottom of the arena
                elif (225 < arena_angle < 315):
                    self.reward -= 2000   
=======
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            self.sumobot_down()
            self.reward -= 0.1
            
        # move top right   
        elif action == 6:     
<<<<<<< HEAD
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 18 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                    #case 6
                    if(180 < angle < 270 and 135 < arena_angle < 210):
                        self.reward += 2000
                    elif (90 < angle < 135 and 90 < arena_angle < 135) or ( angle > 270 and arena_angle > 315):
                        self.reward += 2000
                        
                    elif (angle > 315 and arena_angle < 45) or (90 < angle < 180 and 45 < arena_angle < 90):
                        self.reward += 2000
                        
                    elif (135 < arena_angle < 315):
                        self.reward -= 7000
                else: 
                    if(135 < angle < 315):
                        self.reward += 1000    
                    else: 
                        self.reward -= 2000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                if (135 < arena_angle < 180):
                    self.reward +=2000
                else:
                    self.reward -= 7000
=======
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            self.sumobot_top_right()
            self.reward -= 0.1
            
        # move top left
        elif action == 7:
<<<<<<< HEAD
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 18 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                    #case 9
                    if(180 < angle < 270 and arena_angle > 250):
                        self.reward += 2000
                    elif((angle < 45 or angle > 315) and 45 < arena_angle < 90) or (225 < angle < 270 and 225 < arena_angle < 270):
                        self.reward += 2000
                        
                    elif (180 < angle < 270 and 135 < arena_angle < 180) or (angle < 90 and 90 < arena_angle < 135):
                        self.reward += 2000
                        
                    elif (arena_angle < 45 or arena_angle < 225):
                        self.reward -= 7000
                else:
                    if(angle < 45 or angle > 225):
                        self.reward += 1000
                    else:
                        self.reward -= 1000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                if (315 < arena_angle < 360):
                    self.reward +=1000
                else:
                    self.reward -= 1000
=======
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
            self.sumobot_top_left()
            self.reward -= 0.1
            
        # move bottom right    
        elif action == 8:   
            self.sumobot_bottom_right()
            self.reward -= 0.1
            
        # move bottom left
        elif action == 5:
<<<<<<< HEAD
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 18 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                    #case 11
                    if(270 < angle < 360 and (arena_angle < 90 or arena_angle > 340)):
                        self.reward += 200
                    elif((angle < 45 or angle > 315) and 270 < arena_angle < 315) or (90 < angle < 180 and 135 < arena_angle < 180):
                        self.reward += 2000
                        
                    elif (angle < 270 and 225 < arena_angle < 270) or (90 < angle < 180 and 180 < arena_angle < 225):
                        self.reward += 2000
                        
                    elif (arena_angle > 315 or arena_angle < 135):
                        self.reward -= 7000
                else:
                    if(angle > 315 or angle < 135):
                        self.reward += 2000
                    else:
                        self.reward -= 2000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 33:
                if(0 < arena_angle < 45):
                    self.reward += 1000
                    
                else:
                    self.reward -= 1000
            self.sumobot_bottom_left()            
                        
        self.run_frame()            
=======
            self.sumobot_bottom_left()
            self.reward -= 0.1            

        self.sumobot.setx(self.sumobot.xcor() + self.sumobot.dx)
        self.sumobot.sety(self.sumobot.ycor() + self.sumobot.dy)
        
        self.run_frame()
        
>>>>>>> 0c377e566e5704fafecc702565e7e24e8f12c784
        state = [self.sumobot.xcor(), self.sumobot.ycor(), self.enemy.xcor(), self.enemy.ycor()] # 4
        return self.reward, state, self.done
# ------------------------ Human control ------------------------
#
# env = Sumobot()

# while True:
#      env.run_frame()