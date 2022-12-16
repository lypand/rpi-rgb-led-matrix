#!/usr/bin/env python
from samplebase import SampleBase
from inputs import get_gamepad
import time
from threading import Thread
x = 0
y = 0
clear = False
update = False
class SimpleSquare(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SimpleSquare, self).__init__(*args, **kwargs)

    def run(self):
        global x
        global y
        global clear
        global update
        self.matrix.SetPixel(23, 23, 100, 100, 100)

        while True:
            if update:
                update = False
                print(x, y)
                self.matrix.SetPixel(x, y, 100, 100, 100)
                if clear:
                    print('clearing')
                    self.matrix.Clear()
                    clear = False
            # for x in range(0, offset_canvas.width):
            #     offset_canvas.SetPixel(x, 0, 100, 100, 100)
            #     offset_canvas.SetPixel(x, offset_canvas.height - 1,100, 100, 100)

            # for y in range(0, offset_canvas.height):
            #     offset_canvas.SetPixel(0, y, 100, 100, 100)
            #     offset_canvas.SetPixel(offset_canvas.width - 1, y, 100, 100, 100)

def keyListener():
    global x
    global y
    global clear
    global update
    while 1:
        events = get_gamepad()
        for event in events:
            if event.code == 'ABS_X' and event.state == 0:
                print('Left')
                x = x -1
            if event.code == 'ABS_X' and event.state == 255:
                print('Right')
                x = x + 1
            if event.code == 'ABS_Y' and event.state == 255:
                print('Up')
                y = y + 1
            if event.code == 'ABS_Y' and event.state == 0:
                print('Down')
                y = y - 1
            if event.code == 'MSC_SCAN' and event.state == 589826:
                print('Clear')
                y = 0
                x = 0
                clear = True
            update = True

    
# Main function
if __name__ == "__main__":

    thread = Thread(target = keyListener)
    thread.start()

    simple_square = SimpleSquare()
    if (not simple_square.process()):
        simple_square.print_help()

