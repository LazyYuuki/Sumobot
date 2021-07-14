import turtle as t
import math
import random
import numpy as np
import cmath
from math import sqrt
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
        self.speed = 1
        self.state = [0, 0, 0, 0]

        
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
        self.x = math.sqrt((36**2)/(1 + (math.tan(math.radians(0)))**2))
        self.y = self.x * math.tan(math.radians(0))
        self.sumobot.goto(-self.x,-self.y)
        
        # Enemy
        self.enemy = t.Turtle()
        self.enemy.speed(0)
        self.enemy.shapesize(stretch_wid=0.2, stretch_len=0.2)
        self.enemy.shape('square')
        self.enemy.color('red')
        self.enemy.pu()
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
        
    def enemy_locs(self, xcor, ycor):
        enemy_angle = 0
        dist = [17, 34, 51]
        enemy_angle_delta = 45
        ex = 0
        ey = 0
        for r in dist:  
            while(enemy_angle < 360):
                if enemy_angle <= 90 or enemy_angle > 270: 
                    ex = xcor - math.sqrt((r**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
                    ey = ycor - (ex - xcor) * math.tan(math.radians(enemy_angle)) 
                else:
                    ex = xcor + math.sqrt((r**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
                    ey = ycor + (ex - xcor) * math.tan(math.radians(enemy_angle))  
                    
                if (math.sqrt(ex**2 + ey**2) < self.arena_radius):
                    if 0 <= enemy_angle <= 90:
                        if enemy_angle == 90:
                            self.enemy.goto(ex,-ey-r)
                        else:
                            self.enemy.goto(ex,-ey)
                    elif 90 < enemy_angle <= 180:
                        if enemy_angle == 180:
                            self.enemy.goto(ex-r,ey)
                        self.enemy.goto(ex,ey)
                    elif 180 < enemy_angle <= 270:
                        if enemy_angle == 270:
                            if r == 17 :
                                self.enemy.goto(ex,ey+r)
                            else: 
                                self.enemy.goto(ex,ey)
                        else:
                            self.enemy.goto(ex,ey)
                    elif 270 < enemy_angle <= 360:
                        if enemy_angle == 315:
                            if r == 34:
                                self.enemy.goto(ex,-ey)
                            else:
                                self.enemy.goto(ex,-ey)
                        else:
                            self.enemy.goto(ex,ey)
                else: 
                    pass
#                     self.enemy.pd()
#                     self.enemy.dot('red')
#                     self.enemy.pu()
                enemy_angle += enemy_angle_delta
                time.sleep(0.5)
            enemy_angle -= 360 
    
        
    
    def run_frame(self):
        # Enemy and Arena collision

        if sqrt(pow(self.enemy.xcor(), 2) + pow(self.enemy.ycor(), 2)) > 35:
            # so these two "goto"s should take the values of the particular case we are in
            self.enemy.goto(0, 1)
            self.sumobot.goto(0, 1)
            self.done = True
            
        # Sumobot Arena contact

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 37:
            # so these two "goto"s should take the values of the particular case we are in
            self.sumobot.goto(0, 1)
            self.enemy.goto(0, 1)
            self.reward -= 10000
            self.done = True
        else:
            self.reward += 1000
            
        # stay as far as possible from enemy    
        if sqrt(pow((self.enemy.xcor()-self.sumobot.xcor()), 2) + pow((self.enemy.ycor()-self.sumobot.ycor()), 2)) > 30:
            self.reward += 150
        elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 8:
            self.reward -= 200
        else:
            self.reward += 10
            
        # Enemy Sumobot collision

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 6:
            self.reward -= 1000
        
#         # soon to be giant for loop
#         for i in range(3):
#             self.sumobot.goto(self.radius, 0)
#             while(self.angle < 360):             
#                 self.sumobot_spiral(self.angle, self.radius)
#                 time.sleep(0.5)
#                 self.enemy_locs(self.sumobot.xcor(), self.sumobot.ycor())
#                 self.angle += self.angle_delta
#             self.angle -= 360 
#             self.radius += 10   
            
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
        state = [self.sumobot.xcor(), self.sumobot.ycor(), self.enemy.xcor(), self.enemy.ycor()]
        
        # 0 do nothing
        if action == 0:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) > 30:
                self.reward += 1000
            else:
                self.reward -= 1000
            self.sumobot_stop()
        
        # 1 move left
        elif action == 1:
            #close to the enemy
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 3
                    if(0 < angle < 90 and 70 < arena_angle < 180):
                        self.reward += 2000
                #case of not being close to the arena
                else:
                    # enemy in first and fourth quadrants
                    if angle < 90 or angle > 270:
                        self.reward += 1000
                    # enemy in second and thrid quadrants
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                # robot in first and fourth quadrants edges
                if 135 < arena_angle < 225:
                    self.reward += 4000
            self.sumobot_left()
        
        # 2 move right   
        elif action == 2:
            # close to the enemy
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 2
                    if (90 < angle < 180 and 0 < arena_angle < 110):
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
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                # robot in left side edges
                if arena_angle < 45 or arena_angle > 315:
                    self.reward += 4000
            self.sumobot_right()
  
        # 3 move up  
        elif action == 3:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 5
                    if(90 < angle < 180 and 150 < arena_angle < 225):
                        self.reward += 2000
                # case of not being close to the arena
                else:
                    #enemy below the robot
                    if(180 < angle):
                        self.reward += 1000               
                    #enemy on top of the robot
                    else:
                        self.reward -= 1000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                #robot at the bottom of the arena
                if (225 < arena_angle < 315):
                    self.reward += 1000
            self.sumobot_up()
            
         # 4 move down
        elif action == 4:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 2
                    if (90 < angle < 180 and 0 < arena_angle < 110):
                        self.reward += 2000
                 # case of not being close to the arena
                else:
                    if(45 < angle < 135):
                        self.reward += 1000
                        
                    # elif(angle < 180):
                    #     self.reward -=2000
            #just close to the edge
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                # robot at the top of the arena
                if (45 < arena_angle < 135):
                    self.reward += 1000       
            self.sumobot_down()
            
        # move top right   
        elif action == 6:     
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 6
                    if(180 < angle < 270 and 135 < arena_angle < 210):
                        self.reward += 2000

                    # elif (90 < angle < 135 and 90 < arena_angle < 135) or ( angle > 270 and arena_angle > 315):
                    #     self.reward += 2000
                        
                    # elif (angle > 315 and arena_angle < 45) or (90 < angle < 180 and 45 < arena_angle < 90):
                    #     self.reward += 2000
                        
                    # elif (135 < arena_angle < 315):
                    #     self.reward -= 5000
                else: 
                    if(135 < angle < 315):
                        self.reward += 1000    
                    else: 
                        self.reward -= 2000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                if (135 < arena_angle < 180):
                    self.reward +=2000
                else:
                    self.reward -= 5000
            self.sumobot_top_right()
            
        # move top left
        elif action == 7:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 9
                    if(180 < angle < 270 and arena_angle > 250):
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
            self.sumobot_top_left()
            
            
        # move bottom right    
        elif action == 8:   
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 8
                    if(270 < angle < 360 and 180 < arena_angle < 290):
                        self.reward += 2000
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
            self.sumobot_bottom_right()
            
        # move bottom left
        elif action == 5:
            if sqrt(pow((state[2]-state[0]), 2) + pow((state[3]-state[1]), 2)) < 30 :
                # close to the edge of the arena
                if sqrt(pow(state[0], 2) + pow(state[1], 2)) > 21:
                    #case 11
                    if(270 < angle < 360 and (arena_angle < 90 or arena_angle > 340)):
                        self.reward += 200
                    # elif((angle < 45 or angle > 315) and 270 < arena_angle < 315) or (90 < angle < 180 and 135 < arena_angle < 180):
                    #     self.reward += 2000
                        
                    # elif (angle < 270 and 225 < arena_angle < 270) or (90 < angle < 180 and 180 < arena_angle < 225):
                    #     self.reward += 2000
                        
                    # elif (arena_angle > 315 or arena_angle < 135):
                    #     self.reward -= 5000
                else:
                    if(angle > 315 or angle < 135):
                        self.reward += 2000
                    else:
                        self.reward -= 2000
            elif sqrt(pow(state[0], 2) + pow(state[1], 2)) > 23:
                if(0 < arena_angle < 45):
                    self.reward += 1000
                    
                else:
                    self.reward -= 1000
            self.sumobot_bottom_left()            
                        
        self.run_frame()            
        state = [self.sumobot.xcor(), self.sumobot.ycor(), self.enemy.xcor(), self.enemy.ycor()] # 4
        return self.reward, state, self.done
# ------------------------ Human control ------------------------
#
# env = Sumobot()

# while True:
#      env.run_frame()
        
        
        
    
    
############
# Rough Work
############
#         x = math.sqrt((36**2)/(1 + (math.atan(math.radians(89)))**2))
#         y = x * math.atan(math.radians(89))
#         t.pu()
#         t.goto(-x,-y)
#         print(math.sqrt(x**2 + y**2))
#         t.pd()
#         t.dot('blue')

#         a = 2
#         b = -2*(x + x * (math.tan(0))**2)
#         c = -(7)**2 + (x**2 + (x**2)*(math.tan(0)**2))
#         # calculate the discriminant
#         d = (b**2) - (4*a*c)
#         print(d)

#         # find two solutions
#         sol1 = (-b-cmath.sqrt(d))/(2*a)
#         sol2 = (-b+cmath.sqrt(d))/(2*a)
#         print(sol1, sol2)

#         enemy_angle = 0
#         #0
#         ex = x - math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y - (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(ex,ey)
#         elif 180 < enemy_angle <= 270:
#             t.goto(ex,ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(ex,ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45
        
#         #45
#         ex = x - math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y - (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(ex,ey)
#         elif 180 < enemy_angle <= 270:
#             t.goto(ex,ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(ex,ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45
        
#         #90
#         ex = x - math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y - (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             if enemy_angle == 90:
#                 t.goto(-ex,-ey-14)
#             else:
#                 t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(ex,ey)
#         elif 180 < enemy_angle <= 270:
#             t.goto(ex,ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(ex,ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45
        
#         #135
#         ex = x + math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y + (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(-ex,ey)
#         elif 180 < enemy_angle <= 270:
#             t.goto(ex,ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(ex,ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45
        
#         #180
#         ex = x + math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y + (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(-ex,ey)
#         elif 180 < enemy_angle <= 270:
#             t.goto(ex,ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(ex,ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45
        
#         #225
#         ex = x + math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y + (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(-ex,ey)
#         elif 180 < enemy_angle <= 270:
#             t.goto(-ex,ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(ex,ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45
        
#         #270
#         ex = x + math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y + (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(-ex,ey)
#         elif 180 < enemy_angle <= 270:
#             if enemy_angle == 270:
#                 t.goto(-ex,-ey+14)
#             else:
#                 t.goto(-ex,-ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(ex,ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45
        
#         #315 
#         ex = x - math.sqrt((14**2)/(1+(math.tan(math.radians(enemy_angle))**2)))
#         ey = y - (ex - x) * math.tan(math.radians(enemy_angle))           
#         t.pu()
#         if 0 <= enemy_angle <= 90:
#             t.goto(-ex,-ey)
#         elif 90 < enemy_angle <= 180:
#             t.goto(-ex,ey)
#         elif 180 < enemy_angle <= 270:
#             if enemy_angle == 270:
#                 t.goto(-ex,-ey+14)
#             else:
#                 t.goto(-ex,-ey)
#         elif 270 < enemy_angle <= 360:
#             t.goto(-ex,-ey)
#         t.pd()
#         t.dot('blue')
#         enemy_angle += 45


#         self.x = math.sqrt((36**2)/(1 + (math.tan(math.radians(0)))**2))
#         self.y = self.x * math.tan(math.radians(0))
#         t.pu()
#         t.goto(-self.x,-self.y)
#         t.pd()
#         t.dot('red')  