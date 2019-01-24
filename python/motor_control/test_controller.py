import serial #needed for serial
import time
from pid import PID

def run():
    ArduinoSerial = serial.Serial('com9', 9600) # find right com channel
    time.sleep(2) # wait for connection to be established

    #setup controller
    KP = 1
    KI = 0
    KD = 1

    controller = PID(KP, KI, KD)

    while 1:
        robot_angle = camera.get_robot_angle()
        desired_angle = 45
        control(ArduinoSerial, controller, robot_angle, desired_angle)

        time.sleep(0.1)


def control(serial_com, controller, robot_angle, desired_angle):
    controller.setSetPoint(desired_angle)
    direction = controller.update(robot_angle)
    pace = 1
    serial_com.write(str(direction) + "," + str(pace))


if __name__ == "__main__":
    run()
