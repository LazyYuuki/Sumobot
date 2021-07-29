import turtle as t
import math
from keras.models import load_model
import numpy as np
import time

#load model
model = load_model('modelV3.h5')


win = t.Screen()    # Create a screen
win.title('Paddle')      # Set the title to paddle
win.tracer(0)
t.pu()
t.setpos(-44,0)
t.right(90)
t.pd()
t.circle(44)
t.pu()

# Sumobot
sumobot = t.Turtle()
sumobot.speed(0)
sumobot.shape('square')
sumobot.shapesize(stretch_wid=0.2, stretch_len=0.2)
sumobot.color('blue')
sumobot.pu()
x = math.sqrt((36**2)/(1 + (math.tan(math.radians(0)))**2))
y = x * math.tan(math.radians(0))
sumobot.goto(x,-y)

# Enemy
enemy = t.Turtle()
enemy.speed(0)
enemy.shapesize(stretch_wid=0.2, stretch_len=0.2)
enemy.shape('square')
enemy.color('red')
enemy.pu()
#self.enemy.shapesize(stretch_wid=4, stretch_len=4)

# Paddle Movement
def paddle_right():
    x = enemy.xcor()        # Get the x position of paddle
    enemy.setx(x+1)    # increment the x position by 20

def paddle_left():
    x = enemy.xcor()        # Get the x position of paddle
    enemy.setx(x-1)    # decrement the x position by 20

def paddle_up():
    y = enemy.ycor()        # Get the x position of paddle
    enemy.sety(y+1)    # decrement the x position by 20

def paddle_down():
    y = enemy.ycor()        # Get the x position of paddle
    enemy.sety(y-1)    # decrement the x position by 20

def sumo_stop():
    pass

def sumo_left():
    x = sumobot.xcor()
    sumobot.setx(x - 1)

def sumo_right():
    x = sumobot.xcor()
    sumobot.setx(x + 1)

def sumo_up():
    y = sumobot.ycor()
    sumobot.sety(y + 1)

def sumo_down():
    y = sumobot.ycor()
    sumobot.sety(y - 1)

def sumo_topleft():
    x = sumobot.xcor()
    y = sumobot.ycor()
    sumobot.setx(x - 1)
    sumobot.sety(y + 1)

def sumo_topright():
    x = sumobot.xcor()
    y = sumobot.ycor()
    sumobot.setx(x - 1)
    sumobot.sety(y + 1)

def sumo_botleft():
    x = sumobot.xcor()
    y = sumobot.ycor()
    sumobot.setx(x - 1)
    sumobot.sety(y - 1)

def sumo_botright():
    x = sumobot.xcor()
    y = sumobot.ycor()
    sumobot.setx(x + 1)
    sumobot.sety(y - 1)

while True:
    # Keyboard Control
    win.listen()
    win.onkey(paddle_right, 'Right')   # call paddle_right on right arrow key
    win.onkey(paddle_left, 'Left')     # call paddle_left on right arrow key
    win.onkey(paddle_up, 'Up')     # call paddle_left on right arrow key
    win.onkey(paddle_down, 'Down')     # call paddle_left on right arrow key

    new_list = [sumobot.xcor(), sumobot.ycor(), enemy.xcor(), enemy.ycor()]
    X = np.reshape(new_list, (1, 4))
    pred = model(X)
    move = int(np.argmax(pred[0]))
    if (move == 0):
        sumo_stop()
    if (move == 1):
        sumo_left()
    if (move == 2):
        sumo_right()
    if (move == 3):
        sumo_up()
    if (move == 4):
        sumo_down()
    if (move == 5):
        sumo_topright()
    if (move == 6):
        sumo_topleft()
    if (move == 7):
        sumo_botright()
    if (move == 8):
        sumo_botleft()
    time.sleep(0.1)
    print(move)

    win.update()        # Show the scree continuously 

