import serial #needed for serial
import time
from utils.pid import PID
from utils.camera import Camera
from utils.arduino_connection import Arduino_Connection
from utils.navigation import Navigate
from utils.pick_up_block import pick_up
import cv2

def run():
    arduino = Arduino_Connection(com="com19") # find right com channel

    #setup controller
    KP = 0.75
    KI = 0
    KD = 0.5

    controller = PID(KP, KI, KD)
    camera = Camera(webcam_number=1, return_frame=True)
    position, robot_angle, frame = camera.get_robot_position()
    navigate = Navigate()
    pick_up_drive = pick_up()
    
    cv2.imshow('frame', frame)

    corner = False
    while not corner:
        position, robot_angle, frame = camera.get_robot_position()
        if position:
            corner = navigate.go_to_corner(position, robot_angle)
        else:
            control(arduino, controller, robot_angle, 0)
        time.sleep(0.1)

    line = False
    while not line:
        position, robot_angle, frame = camera.get_robot_position()
        if position:
            line = navigate.go_to_corner(position, robot_angle)
        else:
            control(arduino, controller, robot_angle, 1.57)
        time.sleep(0.1)
    
    while 1:
        position, robot_angle, frame = camera.get_robot_position()
        blocks, blocks_frame = camera.get_block_coords([93, 114])
        cv2.imshow('blocks frame', blocks_frame)
        
        if blocks and position:
            block_data = navigate.calculate_distances_angles(blocks, position, robot_angle)
            best_block = navigate.choose_next_block(block_data, [])
			#print("best")
            print(block_data[best_block][3])
            cv2.circle(blocks_frame, (int(block_data[best_block][0]), int(block_data[best_block][1])), 5, (255,0,0), 3)
            
        cv2.imshow('frame', frame)

        if navigation.block_in_range(block_data, position, robot_angle):
            pick_up_drive.drive_to_collect()

        if block_data and robot_angle:
            desired_angle = block_data[best_block][3] + robot_angle
            control(arduino, controller, robot_angle, desired_angle, debug=True)

        # if block detected, do something

        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


def control(arduino, controller, robot_angle, desired_angle, debug=False):
    controller.setSetPoint(desired_angle)
    direction = controller.update(robot_angle)
    pace = 1
    arduino.drive(direction, pace, debug=True)
    if debug:
        print(direction)
    


if __name__ == "__main__":
    run()
