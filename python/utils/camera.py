import cv2
import numpy as np
import math


class Camera:
    """code for handling camera"""

    def __init__(self, webcam_number, return_frame=False):
        cap = cv2.VideoCapture(webcam_number)  # 0 for internal, 1 for external
        qr_decoder = cv2.QRCodeDetector()
        self.capture = cap
        self.qr_decoder = qr_decoder
        self.return_frame = return_frame

    def get_robot_position(self, robot_position_colour_bounds=np.array([[41, 70], [145, 179]])):
        """returns position and angle of robot
        (x_coord, y_coord), angle_in_deg"""
        _, frame = self.capture.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_green = np.array([robot_position_colour_bounds[0][0], 50, 50])
        upper_green = np.array([robot_position_colour_bounds[0][1], 255, 255])

        lower_purple = np.array([robot_position_colour_bounds[1][0], 50, 50])
        upper_purple = np.array([robot_position_colour_bounds[1][1], 255, 255])

        # Threshold the HSV image to get only blue colors
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)

        # Setup noise reducing variables
        kernel_open = np.ones((5, 5))
        kernel_close = np.ones((10, 10))

        # Reduce noise
        mask_open = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)

        mask_green = mask_close.copy()

        mask_open = cv2.morphologyEx(mask_purple, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)

        mask_purple = mask_close.copy()

        # res = cv2.bitwise_and(frame, frame, mask=mask)
        # res2 = cv2.bitwise_and(frame, frame, mask=mask_close)
        # cv2.imshow('res', res)
        # cv2.imshow('morphology', res2)

        # Get contours
        conts_green, h = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # cv2.drawContours(frame, conts_green, -1, (255, 0, 0), 3)

        conts_purple, h = cv2.findContours(mask_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # cv2.drawContours(frame, conts_purple, -1, (255, 0, 0), 3)

        # List of coords
        blocks = []
        purple_centre_x = 0
        purple_centre_y = 0
        green_centre_x = 0
        green_centre_y = 0
        for i in range(len(conts_green)):
            x, y, w, h = cv2.boundingRect(conts_green[i])
            if 10 < w < 300 and 10 < h < 300:
                blocks.append((x + w / 2, y + h / 2))
                green_centre_x = int(x + w / 2)
                green_centre_y = int(y + h / 2)
                cv2.circle(frame, (green_centre_x, green_centre_y), 5, (0, 0, 255), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for i in range(len(conts_purple)):
            x, y, w, h = cv2.boundingRect(conts_purple[i])
            if 20 < w < 300 and 20 < h < 300:
                blocks.append((x + w / 2, y + h / 2))
                purple_centre_x = int(x + w / 2)
                purple_centre_y = int(y + h / 2)
                cv2.circle(frame, (purple_centre_x, purple_centre_y), 5, (0, 255, 0), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        angle = None
        position = None
        if purple_centre_x > 0 and green_centre_x > 0:
            angle = math.atan2(purple_centre_y - green_centre_y, purple_centre_x - green_centre_x)
            # print(angle * 180 / 3.142)
            position = ((green_centre_x+purple_centre_x)/2, (green_centre_y+purple_centre_y)/2)

        if angle is not None and position is not None:
            if self.return_frame:
                return position, angle, frame
            else:
                return position, angle
        else:
            if self.return_frame:
                return None, None, frame
            else:
                return None, None

    def get_block_coords(self, block_colour_bounds=None):
        """Returns position of blocks as a list of tuples (x, y)"""
        # Get data from webcam
        if block_colour_bounds is None:
            block_colour_bounds = [102, 114]
        _, frame = self.capture.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([block_colour_bounds[0], 50, 50])
        upper_blue = np.array([block_colour_bounds[1], 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Setup noise reducing variables
        kernel_open = np.ones((5, 5))
        kernel_close = np.ones((10, 10))

        # Reduce noise
        mask_open = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)

        res = cv2.bitwise_and(frame, frame, mask=mask)
        res2 = cv2.bitwise_and(frame, frame, mask=mask_close)
        cv2.imshow('res', res)
        cv2.imshow('morphology', res2)

        # Get contours
        conts, h = cv2.findContours(mask_close.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # List of coords
        blocks = []
        for i in range(len(conts)):
            x, y, w, h = cv2.boundingRect(conts[i])
            if 5 < w < 15 and 5 < h < 15:
                blocks.append((x + w / 2, y + h / 2))
                cv2.circle(frame, (int(x + w / 2), int(y + h / 2)), 5, (0, 0, 255), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if self.return_frame:
            return blocks, frame
        else:
            return blocks


def main():
    camera = Camera(0, True)
    while True:
        blocks, frame = camera.get_block_coords()
        position, angle, frame2 = camera.get_robot_position()
        cv2.imshow('frame', frame)
        cv2.imshow('frame2', frame2)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

if __name__ == "__main__":
    main()
