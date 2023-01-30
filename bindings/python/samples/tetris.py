#!/usr/bin/env python
from samplebase import SampleBase
from inputs import get_gamepad
import time
from threading import Thread
import random
import sys
import os
import numpy as np
import copy
from rgbmatrix import graphics
import os

backToMainMenu = False
score = 0
currentShape = None
holdDown = False
holdLeft = False
holdRight = False
frozenLocations = np.full((33,17), False, dtype=bool)
frozenLocations[-1, :] = True
frozenLocations[32, :] = True
frozenLocations[:, 16] = True
gameOver = False
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

class Tetris(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Tetris, self).__init__(*args, **kwargs)

    def start(self):
        global currentShape
        global gameOver
        currentShape = Shape(random.randrange(5,6), self.matrix)
        
        while not gameOver:
            if(currentShape.frozen):
                removeCompletedLines(self.matrix)
                currentShape = Shape(random.randrange(0,6), self.matrix)
                if(currentShape.intersects()):
                    gameOver = True
            time.sleep(1)
            tempCurrentShape = copy.copy(currentShape)
            tempCurrentShape.xOffset += 1
            intersection = tempCurrentShape.intersects()
            if(intersection):
                currentShape.freeze()
            else:
                currentShape.addToX(1)


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

class coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Shape: 

    global frozenLocations

    shapes = [
        [[0, 1, 4, 5]],
        [[1, 5, 9, 13], [4, 5, 6, 7],[2, 6, 10, 14],[8, 9, 10, 11]],                           
        [[0, 1, 5, 9], [3, 7, 6, 5],[6, 10, 14, 15],[12, 8, 9, 10]],
        [[2, 1, 5, 9], [5, 6, 7, 11],[6, 10, 14, 13],[4, 8, 9, 10]],
        [[1, 4, 5, 6], [2, 6, 10, 7], [9, 10, 11, 14], [13, 9, 5, 8]],
        [[1, 5, 4, 8], [1, 2, 6, 7], [7, 11, 10, 14], [8, 9, 13, 14]],
        [[0, 4, 5, 9], [2, 3, 5, 6], [6, 10, 11, 15], [9, 10, 12, 13]]]

    lookupTable = {
        0: coordinate(0, 0),
        1: coordinate(1,0),
        2: coordinate(2,0),
        3: coordinate(3,0),
        4: coordinate(0,1),
        5: coordinate(1,1),
        6: coordinate(2,1),
        7: coordinate(3,1),
        8: coordinate(0,2),
        9: coordinate(1,2),
        10: coordinate(2,2),
        11: coordinate(3,2),
        12: coordinate(0,3),
        13: coordinate(1,3),
        14: coordinate(2,3),
        15: coordinate(3,3),
    }

    colorLookup = [
        [255, 0, 0],
        [255, 255, 0],
        [255, 255, 255],
        [0, 255, 255],
        [0, 0, 255],
        [0, 255, 0],
        [100, 50, 100]]

    def __init__(self, shapeType, matrix):
        self.xOffset = 0
        self.yOffset = 0
        self.shapeType = shapeType
        self.rotation = 0
        self.currentSet = self.shapes[self.shapeType][self.rotation]
        self.shape = self.shapes[self.shapeType]
        self.matrix = matrix
        self.frozen = False
        self.color = self.colorLookup[shapeType]
        if(shapeType is 1): 
            self.color

    def print(self):
        for loc in self.currentSet:
            coordinate = self.lookupTable[loc]
            xValue = coordinate.x + self.xOffset
            yValue = coordinate.y + self.yOffset
            self.matrix.SetPixel(xValue, yValue, self.color[0],self.color[1],self.color[2])

    def clear(self):
        for loc in self.currentSet:
            coordinate = self.lookupTable[loc]
            self.matrix.SetPixel(coordinate.x + self.xOffset, coordinate.y + self.yOffset, 0,0,0)

    def freeze(self):
        self.frozen = True
        for loc in self.currentSet:
            coordinate = self.lookupTable[loc]
            xValue = coordinate.x + self.xOffset
            yValue = coordinate.y + self.yOffset
            frozenLocations[xValue][yValue] = True

    def rotate(self):
        self.clear()
        if(self.rotation + 1 >= len(self.shape)):
            self.rotation = 0
        else: 
            self.rotation += 1
        print(self.rotation)
        self.currentSet = self.shapes[self.shapeType][self.rotation]
        self.print()

    def addToX(self, value):
        self.clear()
        self.xOffset += value
        self.print()

    def addToY(self, value):
        self.clear()
        self.yOffset += value
        self.print()

    def tempRotateCheck(self):
        if(self.rotation + 1 >= len(self.shape)):
            self.rotation = 0
        else: 
            self.rotation += 1
        self.currentSet = self.shapes[self.shapeType][self.rotation]

    def intersects(self):
        for loc in self.currentSet:
            coordinate = self.lookupTable[loc]
            xValue = coordinate.x + self.xOffset
            yValue = coordinate.y + self.yOffset
            if(frozenLocations[xValue][yValue]):
                return True
        return False

def removeCompletedLines(matrix): 
    global frozenLocations;
    global score 
    complete = None
    rowsToRemove = [] 
    for x, sub_list in enumerate(frozenLocations):
        if complete:
            rowsToRemove.append(x-1)
            frozenLocations = np.delete(frozenLocations, x-1, 0)
            row = np.full((1,17), False)
            score = score + 1
            frozenLocations = np.insert(frozenLocations, 0, row, axis=0)
        if x > 31: 
            break
        complete = True
        for y, value in enumerate(sub_list):
            if value == False:
                complete = False  
    printFrozenLocations(matrix)


def printFrozenLocations(matrix):
    global frozenLocations
    for x, sub_list in enumerate(frozenLocations):
        for y, value in enumerate(sub_list):
            matrix.SetPixel(x, y, 0,0,0)
    for x, sub_list in enumerate(frozenLocations):
        for y, value in enumerate(sub_list):
            if(value): 
                matrix.SetPixel(x, y, 34,45,123)

def shapeDown(currentShape):
    global holdDown
    while(holdDown):
        tempCurrentShape = copy.copy(currentShape)
        tempCurrentShape.xOffset += 1
        intersection = tempCurrentShape.intersects()
        if(intersection):
            currentShape.freeze()
        else:
            currentShape.addToX(1)    
        time.sleep(.1) 

def shapeLeft(currentShape):
    global holdLeft
    while(holdLeft):
        tempCurrentShape = copy.copy(currentShape)
        tempCurrentShape.yOffset = tempCurrentShape.yOffset + 1
        intersection = tempCurrentShape.intersects()
        if(not intersection):
            currentShape.addToY(1)    
        time.sleep(.1)   

def shapeRight(currentShape):
    global holdRight
    while(holdRight):
        tempCurrentShape = copy.copy(currentShape)
        tempCurrentShape.yOffset = tempCurrentShape.yOffset - 1
        intersection = tempCurrentShape.intersects()
        if(not intersection):
            currentShape.addToY(-1)    
        time.sleep(.1) 

                    
def keyListener():
    global currentShape
    checkUp = False
    global holdDown
    global holdLeft
    global holdRight
    global gameOver
    global backToMainMenu
    
    while not gameOver or not backToMainMenu:
        events = get_gamepad()
        for event in events:
            #Left
            if event.code == 'ABS_X' and event.state == 0:
                holdLeft = True
                Thread(target = shapeLeft, args=(currentShape,)).start()

            #Right
            if event.code == 'ABS_X' and event.state == 255:
                holdRight = True
                Thread(target = shapeRight, args=(currentShape,)).start()

            #Left + Right reset
            if event.code == 'ABS_X' and event.state == 127:
                holdRight = False
                holdLeft = False

            #Down 
            if event.code == 'ABS_Y' and event.state == 255:
                holdDown = True
                Thread(target = shapeDown, args=(currentShape,)).start()
                
            if event.code == 'ABS_Y' and event.state == 127:
                holdDown = False

            if(checkUp):
                checkUp = False
                if(event.state == 0):
                    tempCurrentShape = copy.copy(currentShape)
                    tempCurrentShape.tempRotateCheck()
                    intersection = tempCurrentShape.intersects()
                    if(not intersection):
                        currentShape.rotate()
            if event.code == 'MSC_SCAN' and event.state == 589826:
                checkUp = True

            if event.code == 'BTN_BASE4' and gameOver:
                backToMainMenu = True

# Main function
if __name__ == "__main__":

    keyListenerThread = Thread(target = keyListener)
    keyListenerThread.start()

    tetris = Tetris()
    matrix = tetris.process()
    try:
        tetris.start()
    except KeyboardInterrupt:
        sys.exit(0)

