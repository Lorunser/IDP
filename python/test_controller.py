import serial #needed for serial
import time
from utils.pid import PID
from utils.camera import Camera
from utils.arduino_connection import Arduino_Connection
import cv2

def run():
    arduino = Arduino_Connection(com="com19") # find right com channel

    #setup controller
    KP = 1
    KI = 0
    KD = 1

    controller = PID(KP, KI, KD)
    camera = Camera(webcam_number=1, return_frame=True)
    position, robot_angle, frame = camera.get_robot_position()
    cv2.imshow('frame', frame)
    while 1:
        position, robot_angle, frame = camera.get_robot_position()
        cv2.imshow('frame', frame)
        desired_angle = 0
        control(arduino, controller, robot_angle, desired_angle, debug=True)

        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


def control(arduino, controller, robot_angle, desired_angle):
    controller.setSetPoint(desired_angle)
    direction = controller.update(robot_angle)
    pace = 0.5
    arduino.drive(direction, pace, debug=True)
    if debug:
        print(direction)
    


if __name__ == "__main__":
    run()
