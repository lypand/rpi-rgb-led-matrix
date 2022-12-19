#!/usr/bin/env python
from samplebase import SampleBase
from inputs import get_gamepad
import time
from threading import Thread
import random

x = 0
y = 0
left = False
right = True
up = False
down = False
delay = .3
snake_body = [[x,y], [x-1,y], [x-2,y]]
fruit_position = [random.randrange(1, 30),random.randrange(1, 14) ]

class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        global x
        global y
        global fruit_position
        snakeLength = 3
        while True:
            self.matrix.Clear()
            self.matrix.SetPixel(fruit_position[0], fruit_position[1], 50, 234, 55)
            for snake in snake_body:
                self.matrix.SetPixel(snake[0], snake[1], 100, 100, 100)
            time.sleep(.05)


def canvasUpdate():
    global left
    global right
    global up
    global down
    global x
    global y
    global fruit_position
    global speed
    fruit_spawn = False
    while 1:
        if(left): 
            x-=1
        if(right): 
            x+=1
        if(up):
            y+=1
        if(down):
            y-=1

        snake_body.insert(0, [x,y])

        if x == fruit_position[0] and y == fruit_position[1]:
            fruit_spawn = True
        else:
            snake_body.pop()

        if(fruit_spawn):
            fruit_position = [random.randrange(1, 30),random.randrange(1, 14) ]
            fruit_spawn = False
        time.sleep(delay)
    

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
    while 1:
        events = get_gamepad()
        for event in events:
            if event.code == 'ABS_X' and event.state == 0:
                print('Left')
                left = True
                right = False
                up = False
                down = False
            if event.code == 'ABS_X' and event.state == 255:
                print('Right')
                left = False
                right = True
                up = False
                down = False
            if event.code == 'ABS_Y' and event.state == 255:
                print('Down')
                left = False
                right = False
                up = True
                down = False
            if event.code == 'ABS_Y' and event.state == 0:
                print('Up')
                left = False
                right = False
                up = False
                down = True
            if event.code == 'MSC_SCAN' and event.state == 589826:
                delay -= .005
    
# Main function
if __name__ == "__main__":

    keyListenerThread = Thread(target = keyListener)
    keyListenerThread.start()

    canvasUpdateThread = Thread(target = canvasUpdate)
    canvasUpdateThread.start()

    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()

