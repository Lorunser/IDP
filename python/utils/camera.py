import cv2
import numpy as np
import math


class Camera:
    """code for handling camera"""

    def __init__(self, webcam_number, return_frame=False):
        cap = cv2.VideoCapture(webcam_number)  # 0 for internal, 1 for external
        cap.set(10, 128) # brightness
        cap.set(11, 128) # contrast
        cap.set(12, 200) # saturation
        self.capture = cap
        self.return_frame = return_frame

    def get_robot_position(self, robot_position_colour_bounds=np.array([[43, 70], [145, 171], [0, 8], [26, 40]]), min_block_size=10, max_block_size=50): # green, pink, orange, yellow
        """returns position and angle of robot
        (x_coord, y_coord), angle_in_deg"""
        _, frame = self.capture.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_green = np.array([robot_position_colour_bounds[0][0], 50, 50])
        upper_green = np.array([robot_position_colour_bounds[0][1], 255, 255])

        lower_pink = np.array([robot_position_colour_bounds[1][0], 50, 50])
        upper_pink = np.array([robot_position_colour_bounds[1][1], 255, 255])

        lower_orange = np.array([robot_position_colour_bounds[2][0], 50, 50])
        upper_orange = np.array([robot_position_colour_bounds[2][1], 255, 255])

        lower_yellow = np.array([robot_position_colour_bounds[3][0], 50, 50])
        upper_yellow = np.array([robot_position_colour_bounds[3][1], 255, 255])

        # Threshold the HSV image to get only blue colors
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        mask_purple = cv2.inRange(hsv, lower_pink, upper_pink)

        mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

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

        mask_open = cv2.morphologyEx(mask_orange, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)

        mask_orange = mask_close.copy()

        mask_open = cv2.morphologyEx(mask_yellow, cv2.MORPH_OPEN, kernel_open)
        mask_close = cv2.morphologyEx(mask_open, cv2.MORPH_CLOSE, kernel_close)

        mask_yellow = mask_close.copy()

        # res = cv2.bitwise_and(frame, frame, mask=mask)
        # res2 = cv2.bitwise_and(frame, frame, mask=mask_close)
        # cv2.imshow('res', res)
        # cv2.imshow('morphology', res2)

        # Get contours
        conts_green, h = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # cv2.drawContours(frame, conts_green, -1, (255, 0, 0), 3)

        conts_purple, h = cv2.findContours(mask_purple, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # cv2.drawContours(frame, conts_purple, -1, (255, 0, 0), 3)

        conts_orange, h = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        conts_yellow, h = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # List of coords
        purple_centre_x = []
        purple_centre_y = []
        green_centre_x = []
        green_centre_y = []
        orange_centre_x = []
        orange_centre_y = []
        yellow_centre_x = []
        yellow_centre_y = []

        for i in range(len(conts_green)):
            x, y, w, h = cv2.boundingRect(conts_green[i])
            if min_block_size < w < max_block_size and min_block_size < h < max_block_size:
                green_centre_x.append(int(x + w / 2))
                green_centre_y.append(int(y + h / 2))
                cv2.circle(frame, (green_centre_x[-1], green_centre_y[-1]), 5, (0, 0, 255), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        for i in range(len(conts_purple)):
            x, y, w, h = cv2.boundingRect(conts_purple[i])
            if min_block_size < w < max_block_size and min_block_size < h < max_block_size:
                purple_centre_x.append(int(x + w / 2))
                purple_centre_y.append(int(y + h / 2))
                cv2.circle(frame, (purple_centre_x[-1], purple_centre_y[-1]), 5, (0, 255, 0), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        for i in range(len(conts_orange)):
            x, y, w, h = cv2.boundingRect(conts_orange[i])
            if min_block_size < w < max_block_size and min_block_size < h < max_block_size:
                orange_centre_x.append(int(x + w / 2))
                orange_centre_y.append(int(y + h / 2))
                cv2.circle(frame, (orange_centre_x[-1], orange_centre_y[-1]), 5, (0, 0, 255), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

        for i in range(len(conts_yellow)):
            x, y, w, h = cv2.boundingRect(conts_yellow[i])
            if min_block_size < w < max_block_size and min_block_size < h < max_block_size:
                yellow_centre_x.append(int(x + w / 2))
                yellow_centre_y.append(int(y + h / 2))
                cv2.circle(frame, (yellow_centre_x[-1], yellow_centre_y[-1]), 5, (0, 255, 0), 3)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)


        # size of robot black sheet: 70x50 pixels
        angle = None
        position = None
        centres = []
        angles = []
        for i in range(len(purple_centre_x)):
            for j in range(len(green_centre_x)):
                if 45 < math.sqrt((purple_centre_x[i]-green_centre_x[j])**2+(purple_centre_y[i]-green_centre_y[j])**2) < 75:
                    midpoint_x = (purple_centre_x[i]+green_centre_x[j])/2
                    midpoint_y = (purple_centre_y[i]+green_centre_y[j])/2
                    angle = math.atan2(purple_centre_y[i] - green_centre_y[j], purple_centre_x[i] - green_centre_x[j])
                    centres.append((midpoint_x-20*math.sin(angle), midpoint_y+20*math.cos(angle)))
                    angles.append(angle)
                    print("1")
                    print(angle)
                    break
            for j in range(len(orange_centre_x)):
                if 60 < math.sqrt((purple_centre_x[i]-orange_centre_x[j])**2+(purple_centre_y[i]-orange_centre_y[j])**2) < 90:
                    midpoint_x = (purple_centre_x[i]+orange_centre_x[j])/2
                    midpoint_y = (purple_centre_y[i]+orange_centre_y[j])/2
                    angle = math.atan2(purple_centre_y[i] - orange_centre_y[j], purple_centre_x[i] - orange_centre_x[j]) +0.6
                    centres.append((midpoint_x, midpoint_y))
                    angles.append(angle)
                    print("2")
                    print(angle)
                    break
            for j in range(len(yellow_centre_x)):
                if 25 < math.sqrt((purple_centre_x[i]-yellow_centre_x[j])**2+(purple_centre_y[i]-yellow_centre_y[j])**2) < 55:
                    midpoint_x = (purple_centre_x[i]+yellow_centre_x[j])/2
                    midpoint_y = (purple_centre_y[i]+yellow_centre_y[j])/2
                    angle = math.atan2(purple_centre_y[i] - yellow_centre_y[j], purple_centre_x[i] - yellow_centre_x[j]) + 1.57
                    centres.append((midpoint_x-30*math.cos(angle), midpoint_y-30*math.sin(angle)))
                    angles.append(angle)
                    print("3")
                    print(angle)
                    break
        for i in range(len(green_centre_x)):
            for j in range(len(yellow_centre_x)):
                if 60 < math.sqrt((green_centre_x[i]-yellow_centre_x[j])**2+(green_centre_y[i]-yellow_centre_y[j])**2) < 90:
                    midpoint_x = (green_centre_x[i]+yellow_centre_x[j])/2
                    midpoint_y = (green_centre_y[i]+yellow_centre_y[j])/2
                    angle = math.atan2(green_centre_y[i] - yellow_centre_y[j], green_centre_x[i] - yellow_centre_x[j])
                    centres.append((midpoint_x, midpoint_y))
                    angles.append(angle)
                    print("4")
                    print(angle)
                    break
            for j in range(len(orange_centre_x)):
                if 25 < math.sqrt((green_centre_x[i]-orange_centre_x[j])**2+(green_centre_y[i]-orange_centre_y[j])**2) < 55:
                    midpoint_x = (green_centre_x[i]+orange_centre_x[j])/2
                    midpoint_y = (green_centre_y[i]+orange_centre_y[j])/2
                    angle = math.atan2(green_centre_y[i] - orange_centre_y[j], green_centre_x[i] - orange_centre_x[j]) + 1.57
                    centres.append((midpoint_x+30*math.cos(angle), midpoint_y+30*math.sin(angle)))
                    angles.append(angle)
                    print("5")
                    print(angle)
        for i in range(len(yellow_centre_x)):
            for j in range(len(orange_centre_x)):
                if 45 < math.sqrt((yellow_centre_x[i]-orange_centre_x[j])**2+(yellow_centre_y[i]-orange_centre_y[j])**2) < 75:
                    midpoint_x = (yellow_centre_x[i]+orange_centre_x[j])/2
                    midpoint_y = (yellow_centre_y[i]+orange_centre_y[j])/2
                    angle = math.atan2(yellow_centre_y[i] - orange_centre_y[j], yellow_centre_x[i] - orange_centre_x[j])
                    centres.append((midpoint_x+20*math.sin(angle), midpoint_y-20*math.cos(angle)))
                    angles.append(angle)
                    print("6")
                    print(angle)

        centres_x = 0
        centres_y = 0
        av_angle = 0
        for centre in centres:
            cv2.circle(frame, (int(centre[0]), int(centre[1])), 4, (0, 255, 0), 2)
            centres_x += centre[0]
            centres_y += centre[1]
        for angle in angles:
            if angle < 0:
                angle += 2*math.pi
            av_angle += angle
        #angle = angles[0]
        
        if len(centres) > 0:
            position = (centres_x/len(centres), centres_y/len(centres))
            angle = av_angle/len(angles)
            if angle > math.pi:
                angle = angle - 2 * math.pi
            #print(angle)
            cv2.circle(frame, (int(position[0]), int(position[1])), 4, (255, 0, 0), 2)
        else:
            position = None
            angle = None
        #if purple_centre_x > 0 and green_centre_x > 0:
        #    angle = math.atan2(purple_centre_y - green_centre_y, purple_centre_x - green_centre_x)
            # print(angle * 180 / 3.142)
        #    position = ((green_centre_x+purple_centre_x)/2, (green_centre_y+purple_centre_y)/2)

        if angle and position:
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
            block_colour_bounds = [91, 114]
        _, frame = self.capture.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of blue color in HSV
        lower_blue = np.array([block_colour_bounds[0], 50, 50])
        upper_blue = np.array([block_colour_bounds[1], 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Setup noise reducing variables
        kernel_open = np.ones((4, 4))
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
    camera = Camera(1, True)
    while True:
        blocks, frame = camera.get_block_coords()
        position, angle, frame2 = camera.get_robot_position()
        #print(angle)
        cv2.rectangle(frame, (25,25), (600,480), (255,0,0), 2)
        cv2.imshow('frame', frame)
        cv2.imshow('frame2', frame2)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

if __name__ == "__main__":
    main()
