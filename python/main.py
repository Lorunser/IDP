import serial #needed for serial
import time
from utils.pid import PID
from utils.camera import Camera
from utils.arduino_connection import Arduino_Connection
from utils.navigation import Navigate
from utils.pick_up_block import pick_up
import cv2
import numpy as np

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
        position, robot_angle, frame = camera.get_robot_position(robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (100,200), 3, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        print(corner)
        if position:
            desired_angle, corner = navigate.go_to_point(position, robot_angle, [100, 200])
            if not corner:
                print(robot_angle)
                control(arduino, controller, robot_angle, desired_angle)
        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    accepted_blocks = 0
    rejected_blocks = 0
    detect_reject = False
    
    while 1:
        position, robot_angle, frame = camera.get_robot_position()
        blocks, blocks_frame = camera.get_block_coords([95, 105])
        cv2.imshow('blocks frame', blocks_frame)

        block_data = None
        
        if blocks and position:
            block_data = navigate.calculate_distances_angles(blocks, position, robot_angle)
            best_block = navigate.choose_next_block(block_data)
			#print("best")
            #print(block_data[best_block][3])
            cv2.circle(blocks_frame, (int(block_data[best_block][0]), int(block_data[best_block][1])), 5, (255,0,0), 3)
            
        cv2.imshow('frame', frame)

        #if navigate.block_in_range(block_data, position, robot_angle):
        #    pick_up_drive.drive_to_collect()

        if block_data and robot_angle:
            desired_angle = block_data[best_block][3] + robot_angle
            control(arduino, controller, robot_angle, desired_angle)

        if arduino.get_block_state() != 0:
            state = arduino.get_block_state()
            print("state: ")
            print(state)
            #if state == 1:
            #    while state == 1:
            #        state = arduino.get_block_state()
            if state == 2:
                accepted_blocks += 1
            if state == 3:
                rejected_blocks += 1
                detect_reject = True

        if detect_reject:
            rejected = navigate.add_block_to_rejects(block_data, position, robot_angle)
            if rejected == True:
                detect_reject = False

        if accepted_blocks >= 5:
            while True:
                relative_angle, arrived = navigate.go_to_point(position, robot_angle, [50, 300])
                if not arrived:
                    desired_angle = relative_angle + robot_angle
                    control(arduino, controller, robot_angle, desired_angle, debug=True)

        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


def control(arduino, controller, robot_angle, desired_angle):
    controller.setSetPoint(desired_angle)
    direction = controller.update(robot_angle)
    pace = 1
    arduino.drive(direction, pace)
    
    


if __name__ == "__main__":
    run()
