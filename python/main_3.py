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
import math

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

    blocks = None
    while blocks == None:
        blocks, blocks_frame = camera.get_block_coords()#[95, 105])
    block_data = navigate.calculate_distances_angles(blocks, position, robot_angle)
    navigate.reject_line(block_data)

    position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        
    cv2.imshow('blocks frame', blocks_frame)

    #block_data = None
        
    if blocks and position:
        block_data = navigate.calculate_distances_angles(blocks, position, robot_angle)
        best_block = navigate.choose_next_block(block_data)
		#print("best")
        #print(block_data[best_block][3])
        cv2.circle(blocks_frame, (int(block_data[best_block][0]), int(block_data[best_block][1])), 5, (255,0,0), 3)
            
    cv2.imshow('frame', frame)

    for block in block_data:
        rejects = navigate.return_rejects()
        arrived = False
        for reject in rejects:
            if abs(block_data[block][0]-reject[0])<30 and abs(block_data[block][0]-reject[0])<30:
                arrived = True
                break
            else:
                arrived = False
        while not arrived:
            position, robot_angle, frame = camera.get_robot_position(robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
            cv2.circle(frame, (int(block_data[block][0]),int(block_data[block][1])), 3, (255, 0, 0), 2)
            cv2.imshow('frame', frame)
            #print(corner)
            if position:
                desired_angle, arrived = navigate.go_to_point(position, robot_angle, [int(block_data[block][0]),int(block_data[block][1])])
                if not arrived:
                    #print(robot_angle)
                    control(arduino, controller, robot_angle, desired_angle)
            time.sleep(0.1)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break

    top_green = False
    while not top_green:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (75,200), 3, (255, 0, 0), 2)
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

    for i in range(50):
        position, robot_angle, frame = camera.get_robot_position()
        if robot_angle:
            control(arduino, controller, robot_angle, -math.pi)
        time.sleep(0.1)
    arduino.open_back_gate()
    arduino.turn_out_left()

    while position[1]< 350:
        position, robot_angle, frame = camera.get_robot_position()
        while position == None:
            position, robot_angle, frame = camera.get_robot_position()
        time.sleep(0.1)

    arduino.close_back_gate()

    corner = False
    while not corner:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (500,60), 3, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        #print(corner)
        if position:
            desired_angle, corner = navigate.go_to_point(position, robot_angle, [500, 60])
            if not corner:
                #print(robot_angle)
                control(arduino, controller, robot_angle, desired_angle)
        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    for i in range(40):
        position, robot_angle, frame = camera.get_robot_position()
        cv2.imshow('frame', frame)
        if robot_angle:
            control(arduino, controller, robot_angle, -math.pi)
        time.sleep(0.1)
    arduino.open_back_gate()
    arduino.turn_out_right()

    while position[1]< 430:
        position, robot_angle, frame = camera.get_robot_position()
        cv2.imshow('frame', frame)
        while position == None:
            position, robot_angle, frame = camera.get_robot_position()
        time.sleep(0.1)

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

    for i in range(30):
        position, robot_angle, frame = camera.get_robot_position()
        cv2.imshow('frame', frame)
        control(arduino, controller, robot_angle, -math.pi)
        time.sleep(0.1)
    arduino.open_back_gate()
    arduino.turn_out_left()

    while position[1]< 350:
        position, robot_angle, frame = camera.get_robot_position()
        cv2.imshow('frame', frame)
        time.sleep(0.1)

    end = False
    while not end:
        position, robot_angle, frame = camera.get_robot_position()#robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [15, 15]]))
        cv2.circle(frame, (50,500), 3, (255, 0, 0), 2)
        cv2.imshow('frame', frame)
        #print(corner)
        if position:
            desired_angle, end = navigate.go_to_point(position, robot_angle, [50, 500])
            if not end:
                #print(robot_angle)
                control(arduino, controller, robot_angle, desired_angle)
        time.sleep(0.1)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    arduino.drive(0,0)
    arduino.close_back_gate()
    

def control(arduino, controller, robot_angle, desired_angle):
    controller.setSetPoint(desired_angle)
    direction = controller.update(robot_angle)
    pace = 1
    arduino.drive(direction, pace)
    
    


if __name__ == "__main__":
    run()
