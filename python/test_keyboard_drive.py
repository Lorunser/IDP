import keyboard
import time
from utils.arduino_connection import Arduino_Connection

pace = 0
direction = 0
STEP = 0.1

def forwards():
    global pace
    pace += STEP
    if (pace > 1):
        pace = 1

def backwards():
    global pace
    pace -= STEP
    if (pace < -1):
        pace = -1
    

def rightwards():
    global direction
    direction += STEP
    if (direction > 1):
        direction = 1


def leftwards():
    global direction
    direction -= STEP
    if (direction < -1):
        direction = -1


def stop():
    global pace
    global direction
    pace = 0
    direction = 0


def run():
    keyboard.add_hotkey('w', forwards)
    keyboard.add_hotkey('a', leftwards)
    keyboard.add_hotkey('s', backwards)
    keyboard.add_hotkey('d', rightwards)

    keyboard.add_hotkey('space', stop)

    arduino = Arduino_Connection(com="com9")

    while (True):
        arduino.drive(direction, pace, debug=True)
        time.sleep(0.1) 


if __name__ == "__main__":
    run()
