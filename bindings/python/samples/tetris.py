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

currentShape = None
frozenLocations = np.full((33,17), False, dtype=bool)
frozenLocations[0, :] = True
frozenLocations[32, :] = True
frozenLocations[:, 16] = True
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

class Tetris(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Tetris, self).__init__(*args, **kwargs)

    def start(self):
        global currentShape
        currentShape = Shape(random.randrange(0,6), self.matrix)
        currentShape.print()

        while True:
            if(currentShape.frozen):
                currentShape = Shape(random.randrange(0,6), self.matrix)
                if(currentShape.intersects()):
                    print("Game Over")
            time.sleep(1)
            tempCurrentShape = copy.copy(currentShape)
            tempCurrentShape.yOffset += 1
            intersection = tempCurrentShape.intersects()
            if(intersection):
                currentShape.freeze()
            else:
                currentShape.addToY(1)

class coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Shape: 

    global frozenLocations

    shapes = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]]]

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

    def __init__(self, shapeType, matrix):
        self.xOffset = 0
        self.yOffset = 0
        self.shapeType = shapeType
        self.rotation = 0
        self.currentSet = self.shapes[self.shapeType][self.rotation]
        self.shape = self.shapes[self.shapeType]
        self.matrix = matrix
        self.frozen = False

    def print(self):
        for loc in self.currentSet:
            coordinate = self.lookupTable[loc]
            xValue = coordinate.x + self.xOffset
            yValue = coordinate.y + self.yOffset
            self.matrix.SetPixel(xValue, yValue, 150,150,150)

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
            frozenLocations[xValue+1][yValue] = True

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

    def intersects(self):
        for loc in self.currentSet:
            coordinate = self.lookupTable[loc]
            xValue = coordinate.x + self.xOffset
            yValue = coordinate.y + self.yOffset
            if(frozenLocations[xValue+1][yValue]):
                return True
        return False                

def keyListener():
    global currentShape
    checkUp = False
    while 1:
        events = get_gamepad()
        for event in events:
            if event.code == 'ABS_X' and event.state == 0:
                tempCurrentShape = copy.copy(currentShape)
                tempCurrentShape.xOffset = tempCurrentShape.xOffset - 1
                intersection = tempCurrentShape.intersects()
                if(not intersection):
                    currentShape.addToX(-1)
            if event.code == 'ABS_X' and event.state == 255:
                tempCurrentShape = copy.copy(currentShape)
                tempCurrentShape.xOffset = tempCurrentShape.xOffset + 1
                intersection = tempCurrentShape.intersects()
                if(not intersection):
                    currentShape.addToX(1)
            if event.code == 'ABS_Y' and event.state == 255:
                tempCurrentShape = copy.copy(currentShape)
                tempCurrentShape.yOffset += 1
                intersection = tempCurrentShape.intersects()
                if(intersection):
                    currentShape.freeze()
                else:
                    currentShape.addToY(1)             
            if(checkUp):
                checkUp = False
                if(event.state == 0):
                    tempCurrentShape = copy.copy(currentShape)
                    if(tempCurrentShape.rotation + 1 >= len(tempCurrentShape.shape)):
                        tempCurrentShape.rotation = 0
                    else: 
                        tempCurrentShape.rotation += 1
                    intersection = tempCurrentShape.intersects()
                    if(intersection):
                        currentShape.freeze()
                    else:
                        currentShape.rotate()
            if event.code == 'MSC_SCAN' and event.state == 589826:
                checkUp = True

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

