import turtle as t
from math import sqrt
import random
import numpy as np
from math import tan

speed = 0.3

class Sumobot():

    def __init__(self):

        self.done = False
        self.reward = 0
        self.enemy_reward = 0
        self.hit, self.miss = 0, 0
        
        t.clearscreen()
        t.pu()
        t.setpos(-40,0) #rememeber to resize 
        t.right(90)
        t.pd()
        t.circle(40) # 40 radius

        t.pu()
        t.goto(0,0)
        t.pd()
        t.dot('red')

        # Setup Background

        self.win = t.Screen()
        self.win.title('Sumobot')
        self.win.setup(width=100, height=100)
        self.win.tracer(0)

        # Sumobot

        self.sumobot = t.Turtle()
        self.sumobot.speed(0)
        self.sumobot.shape('square')
        self.sumobot.shapesize(stretch_wid=0.7, stretch_len=0.7)
        self.sumobot.color('blue')
        self.sumobot.penup()
#         self.sumobot.mode("standard")
        self.sumobot.goto(0, -32) # change this
        self.sumobot.dx = random.randint(0,5)/30
        self.sumobot.dy = random.randint(0,5)/30

        # Enemy

        self.enemy = t.Turtle()
        self.enemy.speed(0)
        self.enemy.shape('square')
        self.enemy.color('red')
        self.enemy.penup()
        self.enemy.shapesize(stretch_wid = 0.9, stretch_len = 0.9)
#         self.enemy.goto(random.randint(0,330), random.randint(0,330))
        self.enemy.goto(0, 30) # change this
        self.enemy.dx = 0
        self.enemy.dy = -1

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

    # Sumobot movement

    def sumobot_right(self):

        self.sumobot.dx = speed
        self.sumobot.dy = 0

    def sumobot_left(self):

        self.sumobot.dx = -speed
        self.sumobot.dy = 0
            
    def sumobot_up(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = speed
    
    def sumobot_down(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = -speed
    
    def sumobot_stop(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = 0
        
    def sumobot_top_right(self):
        self.sumobot.dx = speed
        self.sumobot.dy = speed
        
    def sumobot_top_left(self):
        self.sumobot.dx = -speed
        self.sumobot.dy = speed
        
    def sumobot_bottom_right(self):
        self.sumobot.dx = speed
        self.sumobot.dy = -speed
        
    def sumobot_bottom_left(self):
        self.sumobot.dx = -speed
        self.sumobot.dy = -speed
        
    # Enemy Movement
    
    def enemy_chase(self, sumoX, sumoY):
        angle = self.enemy.towards(sumoX, sumoY)
        if angle == 0:
            self.enemy.dx = 1
            self.enemy.dy = 0
            return
        if 0 < angle < 90:
            X = np.array([[1, 1], [tan(angle), -1]])
            Y = np.array([0.4, 0])
            C = np.linalg.solve(X,Y)
            self.enemy.dx = C[0]
            self.enemy.dy = C[1] 
            return
        if angle == 90:
            self.enemy.dx = 0
            self.enemy.dy = 1
            return
        if 90 < angle < 180:
            angle = angle - 90
            X = np.array([[1, 1], [1, -tan(angle)]])
            Y = np.array([0.4, 0])
            C = np.linalg.solve(X,Y)
            self.enemy.dx = -C[0]
            self.enemy.dy = C[1]  
            return
        if angle == 180:
            self.enemy.dx = -1
            self.enemy.dy = 0
            return
        if 180 < angle < 270:
            angle = angle - 180
            X = np.array([[1, 1], [tan(angle), -1]])
            Y = np.array([0.4, 0])
            C = np.linalg.solve(X,Y)
            self.enemy.dx = -C[0]
            self.enemy.dy = -C[1]
            return
        if angle == 270:
            self.enemy.dx = 0
            self.enemy.dy = -1
            return
        if 270 < angle < 360:
            angle = angle - 270
            X = np.array([[1, 1], [1, -tan(angle)]])
            Y = np.array([0.4, 0])
            C = np.linalg.solve(X,Y)
            self.enemy.dx = C[0]
            self.enemy.dy = -C[1]  
            return
            
    def run_frame(self):

        self.win.update()

        # Sumobot moving
        self.sumobot.setx(self.sumobot.xcor() + self.sumobot.dx)
        self.sumobot.sety(self.sumobot.ycor() + self.sumobot.dy)
        self.enemy_chase(self.sumobot.xcor(), self.sumobot.ycor())
        # Enemy moving
        self.enemy.setx(self.enemy.xcor() + self.enemy.dx)
        self.enemy.sety(self.enemy.ycor() + self.enemy.dy)

        
        # Enemy and Arena collision

        if sqrt(pow(self.enemy.xcor(), 2) + pow(self.enemy.ycor(), 2)) > 30:
            self.sumobot.goto(0, -32)
            self.enemy.goto(0, 30)
            self.miss += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
#             self.enemy_reward -= 1000
            self.done = True
#         else:
#             self.enemy_reward += 400 # always rewarded for being in the arena

        # Sumobot Arena contact

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 32:
            self.sumobot.goto(0, -32)
            self.enemy.goto(0, 30)
            self.miss += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward -= 1000
#             self.enemy_reward += 1000
            self.done = True
        else:
            self.reward += 1000
#             self.enemy_reward -= 400
            
        # stay as far as possible from enemy    
        if sqrt(pow((self.enemy.xcor()-self.sumobot.xcor()), 2) + pow((self.enemy.ycor()-self.sumobot.ycor()), 2)) > 20:
            self.reward += 150
#             self.enemy_reward -= 800
        elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 10:
            self.reward -= 200
#             self.enemy_reward += 600
        else:
            self.reward += 100
#             self.enemy_reward -= 500

        # Enemy Sumobot collision

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 6:
#             self.sumobot.goto(0, -380)
            self.hit += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
            self.reward -= 100
#             self.enemy_reward += 3000
#             self.done = True

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
        self.enemy.goto(0, 30)
#         self.sumobot.right(100)
        return [self.sumobot.xcor(), self.sumobot.ycor(), self.enemy.xcor(), self.enemy.ycor()] # maybe add enemy coordinates too

#     def reset_enemy(self):

#         self.enemy.goto(0, 200)
# #         self.enemy.goto(0, 100)
# #         self.sumobot.right(100)
#         return [self.enemy.xcor(), self.enemy.ycor(), self.enemy.dx, self.enemy.dy]

    def step(self, action):

        self.reward = 0
        self.done = 0
        angle = self.sumobot.towards(self.enemy.xcor(), self.enemy.ycor())
        arena_angle = self.sumobot.towards(0, 0)
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

        state = [self.sumobot.xcor(), self.sumobot.ycor(), self.enemy.xcor(), self.enemy.ycor()] # 6
        return self.reward, state, self.done
    
    
#     def step_enemy(self, action):

#         self.enemy_reward = 0
#         self.done = 0
        
#         if action == 1:
#             angle = self.enemy.towards(self.sumobot.xcor(). self.sumobot.ycor())
#             X = np.array([[1, 1], [1, -tan(360 - angle)]])
#             Y = np.array([2, 0])
#             C = np.linalg.solve(X,Y)
#             self.enemy.dx = C[0]
#             self.enemy.dy = C[1]
#         if action == 0:
#             self.enemy_stop()

#         if action == 1:
#             self.enemy_left()
#             self.enemy_reward += 60
            
#         if action == 2:
#             self.enemy_right()
#             self.enemy_reward += 60
            
#         if action == 3:
#             self.enemy_up()
#             self.enemy_reward += 60
            
#         if action == 4:
#             self.enemy_down()
#             self.enemy_reward += 60
            
#         if action == 5:
#             self.enemy_top_right()
#             self.enemy_reward += 30

#         if action == 6:
#             self.enemy_top_left()
#             self.enemy_reward += 30

#         if action == 7:
#             self.enemy_bottom_right()
#             self.enemy_reward += 30

#         if action == 8:
#             self.enemy_bottom_left()
#             self.enemy_reward += 30
        

#         self.run_frame()

#         state = [self.enemy.xcor(), self.enemy.ycor(), self.enemy.dx, self.enemy.dy] # 4
#         return self.enemy_reward, state, self.done


# ------------------------ Human control ------------------------
#
# env = Sumobot()

# while True:
#      env.run_frame()