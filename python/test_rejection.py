from utils.camera import Camera
from utils.navigation import Navigate
import cv2

def main():
    camera = Camera(1, True)
    while True:
        blocks, frame = camera.get_block_coords()
        position, angle, frame2 = camera.get_robot_position()
        nav = Navigate()
        if blocks and position:
            block_data = nav.calculate_distances_angles(blocks, position, angle)
            print(nav.add_block_to_rejects(block_data, position, angle))
        cv2.imshow('frame', frame)
        cv2.imshow('frame2', frame2)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

if __name__ == "__main__":
    main()