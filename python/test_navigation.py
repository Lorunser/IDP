from utils.camera import Camera
from utils.navigation import Navigate
import cv2

def main():
    camera = Camera(1, True)
    while True:
        blocks, frame = camera.get_block_coords()
        position, angle, frame2 = camera.get_robot_position()
        nav = Navigate()
        #print(blocks)
        if blocks and position:
            block_data = nav.calculate_distances_angles(blocks, position, angle)
            best_block = nav.choose_next_block(block_data, [])
            #print("best")
            #print((int(block_data[best_block][1]), int(block_data[best_block][2])))
            print(block_data[best_block][3])
            cv2.circle(frame2, (int(block_data[best_block][0]), int(block_data[best_block][1])), 5, (255,0,0), 3)
        cv2.imshow('frame', frame)
        cv2.imshow('frame2', frame2)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

if __name__ == "__main__":
    main()