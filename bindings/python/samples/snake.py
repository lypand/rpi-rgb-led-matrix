from samplebase import SampleBase
from inputs import get_gamepad
import time
from threading import Thread
import random
from rgbmatrix import graphics
import os

x = 0
y = 0
left = False
right = True
up = False
down = False
delay = .1
snake_body = [[x,y], [x-1,y], [x-2,y]]
fruit_position = [random.randrange(1, 30),random.randrange(1, 14) ]
matrix = None
gameOver = False
score = 0
lastDirectionCommitted = 'right'
backToMainMenu = False

class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        global x
        global matrix
        global y
        global fruit_position
        global gameOver
        global score
        global backToMainMenu
        matrix = self.matrix
        while not gameOver:
            self.matrix.Clear()
            self.matrix.SetPixel(fruit_position[0], fruit_position[1], 50, 234, 55)
            for snake in snake_body:
                self.matrix.SetPixel(snake[0], snake[1], 100, 100, 100)
            time.sleep(.05)

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        dirname = os.path.dirname(__file__)
        fontFileLocation = os.path.join(dirname, 'fonts/7x13.bdf')
        font.LoadFont(fontFileLocation)
        textColor = graphics.Color(random.randrange(1, 225), random.randrange(1, 225), random.randrange(1, 225))
        pos = offscreen_canvas.width    
        
        while not backToMainMenu:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, "Score: " + str(score) + "  Game Over Press Start.")
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
            time.sleep(0.03)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        offscreen_canvas.Clear()
        self.matrix.Clear()

def canvasUpdate():
    global left
    global right
    global up
    global down
    global x
    global y
    global fruit_position
    global matrix
    global gameOver
    global score
    global lastDirectionCommitted

    fruit_spawn = False
    gameOver = False

    while not gameOver:
        if(left): 
            x-=1
            lastDirectionCommitted = 'left'
        if(right): 
            x+=1
            lastDirectionCommitted = 'right'
        if(up):
            y-=1
            lastDirectionCommitted = 'up'
        if(down):
            y+=1
            lastDirectionCommitted = 'down'

        for location in snake_body:
            if x == location[0] and y == location[1]:
                gameOver = True

        snake_body.insert(0, [x,y])

        if x == fruit_position[0] and y == fruit_position[1]:
            fruit_spawn = True
            score +=1
        else:
            snake_body.pop()

        if(fruit_spawn):
            fruit_position = [random.randrange(1, 30),random.randrange(1, 14) ]
            fruit_spawn = False

        # If we hit the edge then we want to stop the process
        if matrix != None and (x >= matrix.width or x<0 or y >= matrix.height or y < 0):
            gameOver = True
        time.sleep(delay)

def resetVariables():
    global x
    global y
    global left
    global right
    global up
    global down
    global delay
    global snake_body 
    global fruit_position
    global matrix
    global gameOver
    global score
    global lastDirectionCommitted 
    global backToMainMenu
    x = 0
    y = 0
    left = False
    right = True
    up = False
    down = False
    delay = .1
    snake_body = [[x,y], [x-1,y], [x-2,y]]
    fruit_position = [random.randrange(1, 30),random.randrange(1, 14) ]
    matrix = None
    gameOver = False
    score = 0
    lastDirectionCommitted = 'right'
    backToMainMenu = False
def keyListener():
    global x
    global y
    global clear
    global update
    global left
    global right
    global up
    global down
    global delay
    global gameOver
    global backToMainMenu

    gameOver = False
    while not gameOver or not backToMainMenu:
        events = get_gamepad()

        for event in events:
            if event.code == 'ABS_X' and event.state == 0 and lastDirectionCommitted != 'right':
                left = True
                right = False
                up = False
                down = False
            if event.code == 'ABS_X' and event.state == 255 and lastDirectionCommitted != 'left':
                left = False
                right = True
                up = False
                down = False
            if event.code == 'ABS_Y' and event.state == 255 and lastDirectionCommitted != 'up':
                left = False
                right = False
                up = False
                down = True
            if event.code == 'ABS_Y' and event.state == 0 and lastDirectionCommitted != 'down':
                left = False
                right = False
                up = True
                down = False
            if event.code == 'MSC_SCAN' and event.state == 589826:
                delay -= .005
            if event.code == 'BTN_BASE4' and gameOver:
                backToMainMenu = True
    
# Main function
if __name__ == "__main__":
    keyListenerThread = Thread(target = keyListener)
    keyListenerThread.start()

    canvasUpdateThread = Thread(target = canvasUpdate)
    canvasUpdateThread.start()

    simple_square = SimpleSquare()
    simple_square.process()

