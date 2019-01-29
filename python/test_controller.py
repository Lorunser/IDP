import serial #needed for serial
import time
from utils.pid import PID
from utils.camera import Camera
from utils.arduino_connection import Arduino_Connection

def run():
    arduino = Arduino_Connection(com="com9") # find right com channel
    time.sleep(2) # wait for connection to be established

    #setup controller
    KP = 1
    KI = 0
    KD = 1

    controller = PID(KP, KI, KD)
    camera = Camera(webcam_number=1)

    while 1:
        position, robot_angle = camera.get_robot_position()
        desired_angle = 0
        control(arduino, controller, robot_angle, desired_angle)

        time.sleep(0.1)


def control(arduino, controller, robot_angle, desired_angle):
    controller.setSetPoint(desired_angle)
    direction = controller.update(robot_angle)
    pace = 1
    arduino.drive(direction, pace)


if __name__ == "__main__":
    run()
