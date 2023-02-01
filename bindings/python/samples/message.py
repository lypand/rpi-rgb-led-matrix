from samplebase import SampleBase
from inputs import get_gamepad
import time
from threading import Thread
import random
from rgbmatrix import graphics
import os

currentLetterPosition = 0
letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","_", ".", "!", "?", "1", "2","3","4","5","6","7","8","9"]
word = ""
wordComplete = False
backToMainMenu = False
sleepSpeed = .03
textColor = graphics.Color(random.randrange(1, 225), random.randrange(1, 225), random.randrange(1, 225))

class Message(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Message, self).__init__(*args, **kwargs)

    def run(self):

        global currentLetterPosition
        global letters
        global word
        global matrix
        global canvas
        global font
        
        matrix = self.matrix
        canvas =  self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        dirname = os.path.dirname(__file__)
        fontFileLocation = os.path.join(dirname, 'fonts/7x13.bdf')
        font.LoadFont(fontFileLocation)
        textColor = graphics.Color(150, 150, 150)
        pos = canvas.width / 2 - 3  
        graphics.DrawText(canvas, font, pos, 12, textColor, letters[currentLetterPosition])
        canvas = self.matrix.SwapOnVSync(canvas)
        #offscreen_canvas.Clear()

def keyListener():
    global currentLetterPosition
    global letters
    global word
    global matrix
    global canvas
    global font
    global wordComplete
    global backToMainMenu
    global sleepSpeed
    global textColor

    while not wordComplete:
        events = get_gamepad()
        for event in events:
            if event.code == 'ABS_Y' and event.state == 255 and len(letters) -1 > currentLetterPosition:
                currentLetterPosition = currentLetterPosition + 1
                write()
            if event.code == 'ABS_Y' and event.state == 0 and 0 < currentLetterPosition:
                currentLetterPosition = currentLetterPosition - 1
                write()
            if event.code == 'BTN_THUMB' and event.state == 1:
                if(letters[currentLetterPosition] != "_"):
                    word = word + letters[currentLetterPosition]
                else: 
                    word = word + " "

            if event.code == 'BTN_BASE4':
                wordComplete = True

    pos = canvas.width / 2 - 3 
    Thread(target = mainMenu).start()

    while not backToMainMenu:
        canvas.Clear()
        length = graphics.DrawText(canvas, font, pos, 12, textColor, word)
        pos -= 1
        if (pos + length < 0):
            pos = canvas.width
        time.sleep(sleepSpeed)
        canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

def resetVariables():
    global currentLetterPosition
    global letters
    global word
    global matrix
    global canvas
    global font
    global wordComplete
    global backToMainMenu
    global sleepSpeed

    currentLetterPosition = 0
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z","_", ".", "!", "?", "1", "2","3","4","5","6","7","8","9"]
    word = ""
    wordComplete = False
    backToMainMenu = False
    sleepSpeed = .03

def mainMenu():
    global canvas
    global backToMainMenu
    global sleepSpeed
    global textColor

    while not backToMainMenu:
        events = get_gamepad()
        for event in events:
            if event.code == 'ABS_Y' and event.state == 255:  
                sleepSpeed = sleepSpeed + .003  
            if event.code == 'ABS_Y' and event.state == 0 and sleepSpeed > .003:
                sleepSpeed = sleepSpeed - .003
            if event.code == 'ABS_X' and event.state == 255:
                textColor = graphics.Color(random.randrange(1, 225), random.randrange(1, 225), random.randrange(1, 225))
            if event.code == 'ABS_X' and event.state == 0:
                textColor = graphics.Color(random.randrange(1, 225), random.randrange(1, 225), random.randrange(1, 225))
            if event.code == 'BTN_BASE4'and event.state == 1:
                backToMainMenu = True
    canvas.Clear()



def write():
    global currentLetterPosition
    global letters
    global matrix
    global canvas
    global font
    canvas.Clear()
    pos = canvas.width / 2 - 3 
    textColor = graphics.Color(150, 150, 150)
    graphics.DrawText(canvas, font, pos, 12, textColor, letters[currentLetterPosition])
    canvas = matrix.SwapOnVSync(canvas)

