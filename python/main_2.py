import serial #needed for serial
import time
from utils.pid import PID
from utils.camera import Camera
from utils.arduino_connection import Arduino_Connection
from utils.navigation import Navigate
from utils.pick_up_block import pick_up
import cv2
import numpy as np
from enum import Enum

class Block_States(Enum):
    """Classify data recived from Arduino"""
    NO_BLOCK = 0
    BLOCK_DETECTED = 1
    BLOCK_ACCEPTED = 2
    BLOCK_REJECTED = 3

def run():
    arduino = Arduino_Connection(com="com19") # find right com channel

    #setup controller
    KP = 0.75
    KI = 0
    KD = 0.75

    controller = PID(KP, KI, KD)
    camera = Camera(webcam_number=1, return_frame=True)
    position, robot_angle, frame = camera.get_robot_position()
    navigate = Navigate()
    pick_up_drive = pick_up()
    
    cv2.imshow('frame', frame)

    blocks, blocks_frame = camera.get_block_coords()#[95, 105])
    block_data = navigate.calculate_distances_angles(blocks, position, robot_angle)
    navigate.reject_line(block_data)

    corner = False
    while not corner:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (520,60), 3, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        #print(corner)
        if position:
            desired_angle, corner = navigate.go_to_point(position, robot_angle, [520, 60])
            if not corner:
                #print(robot_angle)
                control(arduino, controller, robot_angle, desired_angle)
        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    top_line = False
    while not top_line:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (530,130), 3, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        #print(corner)
        if position:
            desired_angle, top_line = navigate.go_to_point(position, robot_angle, [530, 130])
            if not top_line:
                #print(robot_angle)
                control(arduino, controller, robot_angle, desired_angle)
        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    mid_line = False
    while not mid_line:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (530,430), 3, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        #print(corner)
        if position:
            desired_angle, mid_line = navigate.go_to_point(position, robot_angle, [530, 280])
            if not mid_line:
                #print(robot_angle)
                control(arduino, controller, robot_angle, desired_angle)
        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    bottom_line = False
    while not bottom_line:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (530,430), 3, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        #print(corner)
        if position:
            desired_angle, bottom_line = navigate.go_to_point(position, robot_angle, [530, 430])
            if not bottom_line:
                #print(robot_angle)
                control(arduino, controller, robot_angle, desired_angle)
        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    accepted_blocks = 0
    rejected_blocks = 0
    detect_reject = False
    
    
    while 1:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        
        cv2.imshow('blocks frame', blocks_frame)

        block_data = None
        
        if blocks and position:
            block_data = navigate.calculate_distances_angles(blocks, position, robot_angle)
            best_block = navigate.choose_next_block(block_data)
			#print("best")
            #print(block_data[best_block][3])
            cv2.circle(blocks_frame, (int(block_data[best_block][0]), int(block_data[best_block][1])), 5, (255,0,0), 3)
            
        cv2.imshow('frame', frame)

        for block in block_data:
            arrived = False
            while not arrived:
                position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
                cv2.circle(frame, (int(block_data[block][0]),int(block_data[block][1])), 3, (255, 0, 0), 2)
                cv2.imshow('frame', frame)
                #print(corner)
                if position:
                    desired_angle, arrived = navigate.go_to_point(position, robot_angle, [int(block_data[block][0]),int(block_data[block][1])])
                    if not arrived:
                        #print(robot_angle)
                        control(arduino, controller, robot_angle, desired_angle)

        top_green = False
        while not top_green:
            position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
            cv2.circle(frame, (50,200), 3, (255, 0, 0), 2)
            cv2.imshow('frame', frame)
            #print(corner)
            if position:
                desired_angle, top_green = navigate.go_to_point(position, robot_angle, [50, 200])
                if not top_green:
                    #print(robot_angle)
                    control(arduino, controller, robot_angle, desired_angle)
            time.sleep(0.1)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

        green = False
        while not green:
            position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
            cv2.circle(frame, (50,250), 3, (255, 0, 0), 2)
            cv2.imshow('frame', frame)
            #print(corner)
            if position:
                desired_angle, green = navigate.go_to_point(position, robot_angle, [50, 250])
                if not green:
                    #print(robot_angle)
                    control(arduino, controller, robot_angle, desired_angle)
            time.sleep(0.1)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        arduino.open_back_gate()

        end = False
        while not end:
            position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
            cv2.circle(frame, (50,450), 3, (255, 0, 0), 2)
            cv2.imshow('frame', frame)
            #print(corner)
            if position:
                desired_angle, end = navigate.go_to_point(position, robot_angle, [50, 450])
                if not end:
                    #print(robot_angle)
                    control(arduino, controller, robot_angle, desired_angle)
            time.sleep(0.1)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        arduino.drive(0,0)
        break

        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break


def control(arduino, controller, robot_angle, desired_angle):
    controller.setSetPoint(desired_angle)
    direction = controller.update(robot_angle)
    pace = 0.7
    arduino.drive(direction, pace)
    
    


if __name__ == "__main__":
    run()
