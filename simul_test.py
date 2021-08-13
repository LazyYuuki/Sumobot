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
        self.sumobot.goto(0, 30)
        self.sumobot.dx = 0
        self.sumobot.dy = 0
        
        # Enemy
        self.enemy = t.Turtle()
        self.enemy.speed(0)
        self.enemy.shapesize(stretch_wid=0.2, stretch_len=0.2)
        self.enemy.shape('square')
        self.enemy.color('red')
        self.enemy.pu()
        self.enemy.goto(0,-30)
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
        
        scale = 1/sqrt(pow(dx,2) + pow(dy,2))
        
        self.enemy.dx = dx * scale
        self.enemy.dy = dy * scale
        
        # print(angle, distance, self.enemy.dx, self.enemy.dy)
        
        self.enemy.setx(self.enemy.xcor() + self.enemy.dx)
        self.enemy.sety(self.enemy.ycor() + self.enemy.dy)
            
        # Sumobot Arena contact
        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 34:
            # so these two "goto"s should take the values of the particular case we are in
            self.reward -= 30
            self.done = 1
        else:
            if sqrt(pow(self.enemy.xcor() - self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 20:
                # so these two "goto"s should take the values of the particular case we are in
                self.reward -= 30
                self.done = 1
            else:
                self.reward += 1
            
        # stay as far as possible from enemy    
        # if  sqrt(pow(self.enemy.xcor() - self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 20:
        #    self.reward -= 100
            
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
        
        self.speed = random.randint(3, 6)
        
        # 0 do nothing
        if action == 0:
            self.sumobot_stop()
        
        # 1 move left
        elif action == 1:
            self.sumobot_left()
            self.reward -= 0.2
        
        # 2 move right   
        elif action == 2:
            self.sumobot_right()
            self.reward -= 0.2
  
        # 3 move up  
        elif action == 3:
            self.sumobot_up()
            self.reward -= 0.2
            
         # 4 move down
        elif action == 4:
            self.sumobot_down()
            self.reward -= 0.2
            
        # move top right   
        elif action == 5:     
            self.sumobot_top_right()
            self.reward -= 0.2
            
        # move top left
        elif action == 6:
            self.sumobot_top_left()
            self.reward -= 0.2
            
        # move bottom right    
        elif action == 7:   
            self.sumobot_bottom_right()
            self.reward -= 0.2
            
        # move bottom left
        elif action == 8:
            self.sumobot_bottom_left()
            self.reward -= 0.2            

        self.sumobot.setx(self.sumobot.xcor() + self.sumobot.dx)
        self.sumobot.sety(self.sumobot.ycor() + self.sumobot.dy)
        
        self.run_frame()
        
        state = [self.sumobot.xcor(), self.sumobot.ycor(), self.enemy.xcor(), self.enemy.ycor()] # 4
        return self.reward, state, self.done
# ------------------------ Human control ------------------------
#
# env = Sumobot()

# while True:
#      env.run_frame()