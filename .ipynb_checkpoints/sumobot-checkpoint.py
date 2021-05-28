import turtle as t
from math import sqrt
import random
import numpy as np
from math import tan



class Sumobot():

    def __init__(self):

        self.done = False
        self.reward = 0
        self.enemy_reward = 0
        self.hit, self.miss = 0, 0
        
        t.clearscreen()
        t.pu()
        t.setpos(-400,0)
        t.right(90)
        t.pd()
        t.circle(400)

        t.pu()
        t.goto(0,0)
        t.pd()
        t.dot('red')

        # Setup Background

        self.win = t.Screen()
        self.win.title('Sumobot')
        self.win.setup(width=1000, height=1000)
        self.win.tracer(0)

        # Sumobot

        self.sumobot = t.Turtle()
        self.sumobot.speed(0)
        self.sumobot.shape('square')
        self.sumobot.shapesize(stretch_wid=2, stretch_len=2)
        self.sumobot.color('blue')
        self.sumobot.penup()
#         self.sumobot.mode("standard")
        self.sumobot.goto(0, -380)
        self.sumobot.dx = random.randint(0,4)
        self.sumobot.dy = random.randint(0,4)

        # Enemy

        self.enemy = t.Turtle()
        self.enemy.speed(0)
        self.enemy.shape('square')
        self.enemy.color('red')
        self.enemy.penup()
        self.enemy.shapesize(stretch_wid=4, stretch_len=4)
#         self.enemy.goto(random.randint(0,330), random.randint(0,330))
        self.enemy.goto(0, 200)
        self.enemy.dx = 0
        self.enemy.dy = -1

        # Score

        self.score = t.Turtle()
        self.score.speed(0)
        self.score.color('black')
        self.score.penup()
        self.score.hideturtle()
        self.score.goto(0, 250)
        self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))

        # -------------------- Keyboard control ----------------------

#         self.win.listen()
#         self.win.onkey(self.sumobot_right, 'Right')
#         self.win.onkey(self.sumobot_left, 'Left')
#         self.win.onkey(self.sumobot_up, 'Up')
#         self.win.onkey(self.sumobot_down, 'Down')

    # Sumobot movement

    def sumobot_right(self):

        self.sumobot.dx = 3
        self.sumobot.dy = 0

    def sumobot_left(self):

        self.sumobot.dx = -3
        self.sumobot.dy = 0
            
    def sumobot_up(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = 3
    
    def sumobot_down(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = -3
    
    def sumobot_stop(self):
        
        self.sumobot.dx = 0
        self.sumobot.dy = 0
        
    def sumobot_top_right(self):
        self.sumobot.dx = 3
        self.sumobot.dy = 3
        
    def sumobot_top_left(self):
        self.sumobot.dx = -3
        self.sumobot.dy = 3
        
    def sumobot_bottom_right(self):
        self.sumobot.dx = 3
        self.sumobot.dy = -3
        
    def sumobot_bottom_left(self):
        self.sumobot.dx = -3
        self.sumobot.dy = -3
        
    # Enemy Movement
    
    def enemy_chase(self, sumoX, sumoY):
        angle = self.enemy.towards(sumoX, sumoY)
        if angle == 0:
            self.enemy.dx = 1
            self.enemy.dy = 0
            return
        if 0 < angle < 90:
            X = np.array([[1, 1], [tan(angle), -1]])
            Y = np.array([2, 0])
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
            Y = np.array([2, 0])
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
            Y = np.array([2, 0])
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
            Y = np.array([2, 0])
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

        if sqrt(pow(self.enemy.xcor(), 2) + pow(self.enemy.ycor(), 2)) > 340:
            self.enemy.goto(0, 200)
            self.sumobot.goto(0, -380)
            self.miss += 1
            self.score.clear()
            self.score.write("Hit: {}   Missed: {}".format(self.hit, self.miss), align='center', font=('Courier', 24, 'normal'))
#             self.enemy_reward -= 1000
            self.done = True
#         else:
#             self.enemy_reward += 400 # always rewarded for being in the arena

        # Sumobot Arena contact

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.sumobot.ycor(), 2)) > 382:
            self.sumobot.goto(0, -380)
            self.enemy.goto(0, 200)
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
        if sqrt(pow((self.enemy.xcor()-self.sumobot.xcor()), 2) + pow((self.enemy.ycor()-self.sumobot.ycor()), 2)) > 300:
            self.reward += 150
#             self.enemy_reward -= 800
        elif sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80:
            self.reward -= 200
#             self.enemy_reward += 600
        else:
            self.reward += 100
#             self.enemy_reward -= 500

        # Enemy Sumobot collision

        if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 60:
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

        self.sumobot.goto(0, -380)
        self.enemy.goto(0, 200)
#         self.sumobot.right(100)
        return [self.sumobot.xcor(), self.sumobot.ycor(), self.sumobot.dx, self.sumobot.dy] # maybe add enemy coordinates too

#     def reset_enemy(self):

#         self.enemy.goto(0, 200)
# #         self.enemy.goto(0, 100)
# #         self.sumobot.right(100)
#         return [self.enemy.xcor(), self.enemy.ycor(), self.enemy.dx, self.enemy.dy]

    def step(self, action):

        self.reward = 0
        self.done = 0
        angle = self.sumobot.towards(self.enemy.xcor(), self.enemy.ycor())
        if action == 0:
            self.sumobot_stop()
#             if sqrt(pow((self.enemy.xcor()-self.sumobot.xcor()), 2) + pow((self.enemy.ycor()-self.sumobot.ycor()), 2)) > 300:
#                 self.reward += 200
#             else:
#                 self.reward -= 100

        if action == 1:
            self.sumobot_left()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80:
                if angle < 90 or angle > 270:
                    self.reward += 1000
                else:
                    self.reward -= 1000
            else:
                self.reward += 60
                          
        if action == 2:
            self.sumobot_right()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80:
                if angle < 90 or angle > 270:
                    self.reward -= 1000
                else:
                    self.reward += 1000
            self.reward += 60
            
        if action == 3:
            self.sumobot_up()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80:
                if 180 < angle:
                    self.reward += 1000
                else:
                    self.reward -= 1000
            else: 
                self.reward += 60
            
        if action == 4:
            self.sumobot_down()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80:
                if 180 < angle:
                    self.reward -= 1000
                else:
                    self.reward += 1000
            else: 
                self.reward += 60
            
        if action == 5:
            self.sumobot_top_right()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80: 
                if 180 < angle < 270:
                    self.reward += 1000
                elif angle < 90:
                    self.reward -= 1000
            else:
                self.reward += 30

        if action == 6:
            self.sumobot_top_left()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80: 
                if angle > 270:
                    self.reward += 1000
                elif 90 < angle < 180:
                    self.reward -= 1000
            else:
                self.reward += 30

        if action == 7:
            self.sumobot_bottom_right()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80: 
                if 90 < angle < 180:
                    self.reward += 1000
                elif angle < 270:
                    self.reward -= 1000
            else:
                self.reward += 30
            

        if action == 8:
            self.sumobot_bottom_left()
            if sqrt(pow(self.sumobot.xcor(), 2) + pow(self.enemy.ycor() - self.sumobot.ycor(), 2)) < 80: 
                if angle < 90:
                    self.reward += 1000
                elif 180 < angle < 270:
                    self.reward -= 1000
            else:
                self.reward += 30
        

        self.run_frame()

        state = [self.sumobot.xcor(), self.sumobot.ycor(), self.sumobot.dx, self.sumobot.dy] # 4
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