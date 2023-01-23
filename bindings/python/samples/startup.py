#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics
import time
from threading import Thread
from inputs import get_gamepad
import random
import snake
import tetris
from enum import Enum
import os

class GameOptions(Enum):
    SNAKED = 0
    TETRIS = 1

currentPos = 0
generateNewColor = True
selectionMade = False
currentSelection = GameOptions.SNAKED

class StartUp(SampleBase):
    def __init__(self, *args, **kwargs):
        super(StartUp, self).__init__(*args, **kwargs)

    def run(self):
        global currentSelection
        global generateNewColor
        global selectionMade
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        dirname = os.path.dirname(__file__)
        fontFileLocation = os.path.join(dirname, 'fonts/8x13.bdf')

        font.LoadFont(fontFileLocation)
        textColor = graphics.Color(random.randrange(1, 225), random.randrange(1, 225), random.randrange(1, 225))
        pos = offscreen_canvas.width

        while not selectionMade:
            offscreen_canvas.Clear()
            if(generateNewColor):
                textColor = graphics.Color(random.randrange(1, 225), random.randrange(1, 225), random.randrange(1, 225))
                generateNewColor = False

            len = graphics.DrawText(offscreen_canvas, font, pos, 12, textColor, currentSelection.name)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        return currentSelection.value

def keyListener():
    global currentSelection
    global generateNewColor
    global selectionMade
    while not selectionMade:
        events = get_gamepad()
        print("Main key listener")
        for event in events:
            if event.code == 'ABS_Y' and event.state == 255:
                currentSelection = GameOptions((currentSelection.value + 1) % (len(GameOptions)))
                generateNewColor = True
            if event.code == 'ABS_Y' and event.state == 0:
                currentSelection = GameOptions((currentSelection.value - 1) % (len(GameOptions)))
                generateNewColor = True
            if event.code == 'MSC_SCAN' and event.state == 589826:
                selectionMade = True

def resetVariables():
    global generateNewColor
    global selectionMade
    generateNewColor = True
    selectionMade = False

# Main function
if __name__ == "__main__":


    while(True):

        resetVariables()

        mainThreadKeyListener = Thread(target=keyListener)
        mainThreadKeyListener.start()
        selection = StartUp().process()
        mainThreadKeyListener.join()

        if selection == 0:
            snake.resetVariables()
            keyListenerThread = Thread(target = snake.keyListener)
            keyListenerThread.start()

            canvasUpdateThread = Thread(target = snake.canvasUpdate)
            canvasUpdateThread.start()

            simple_square = snake.SimpleSquare()
            simple_square.process()

            keyListenerThread.join()
            canvasUpdateThread.join()

        if selection == 1:
            keyListenerThread = Thread(target = tetris.keyListener)
            keyListenerThread.start()
            tetris = tetris.Tetris()
            matrix = tetris.process()
            tetris.start()
    
