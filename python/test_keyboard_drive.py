import keyboard
import time
from utils.arduino_connection import Arduino_Connection

pace = 0
direction = 0
STEP = 0.1

arduino = Arduino_Connection(com="com5")

def forwards():
    global pace
    pace += STEP
    if (pace > 1):
        pace = 1
        print("FULL SPEED AHEAD")

def backwards():
    global pace
    pace -= STEP
    if (pace < -1):
        pace = -1
        print("BACK IT UP")
    

def rightwards():
    global direction
    direction += STEP
    if (direction > 1):
        direction = 1
        print("MAX RIGHT")


def leftwards():
    global direction
    direction -= STEP
    if (direction < -1):
        direction = -1
        print("MAX LEFT")


def stop():
    global pace
    global direction
    pace = 0
    direction = 0
    print("STOP")


def send():
    global arduino
    global pace
    global direction
    arduino.drive(direction, pace, debug=False)


def run():
    keyboard.add_hotkey('w', forwards)
    keyboard.add_hotkey('a', leftwards)
    keyboard.add_hotkey('s', backwards)
    keyboard.add_hotkey('d', rightwards)

    keyboard.add_hotkey('space', stop)

    keyboard.add_hotkey('enter', send)


    while (True):
        send()
        time.sleep(0.01)


if __name__ == "__main__":
    run()
