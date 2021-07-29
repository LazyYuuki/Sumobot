import turtle

win = turtle.Screen()    # Create a screen
win.title('Paddle')      # Set the title to paddle
win.bgcolor('black')     # Set the color to black
win.tracer(0)
win.setup(width=600, height=600)   # Set the width and height to 600

# Paddle
paddle = turtle.Turtle()    # Create a turtle object
paddle.shape('square')      # Select a square shape
paddle.speed(0)             
paddle.shapesize(stretch_wid=1, stretch_len=5)   # Streach the length of square by 5 
paddle.penup()
paddle.color('white')       # Set the color to white
paddle.goto(0, -275)        # Place the shape on bottom of the screen

# Ball
ball = turtle.Turtle()      # Create a turtle object
ball.speed(0)
ball.shape('circle')        # Select a circle shape
ball.color('red')           # Set the color to red
ball.penup()
ball.goto(0, 100)           # Place the shape in middle

# Paddle Movement
def paddle_right():
    x = paddle.xcor()        # Get the x position of paddle
    if x < 225:
        paddle.setx(x+20)    # increment the x position by 20

def paddle_left():
    x = paddle.xcor()        # Get the x position of paddle
    if x > -225:
        paddle.setx(x-20)    # decrement the x position by 20



while True:
    win.update()        # Show the scree continuously 
    # Keyboard Control
    win.listen()
    win.onkey(paddle_right, 'Right')   # call paddle_right on right arrow key
    win.onkey(paddle_left, 'Left')     # call paddle_left on right arrow key
