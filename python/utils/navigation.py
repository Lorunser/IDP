import math


class Navigate:
    """Code for choosing the next block to travel to and return relative angle and distance"""

    def __init__(self):
        self.reject_blocks = {}

    def calculate_distances_angles(self, blocks, position, robot_angle):
        """Return array of distances and relative angles"""
        block_data = {}
        data = []
        for block in blocks:
            # data = [block[0], block[1]]
            distance = math.sqrt(((block[0]-position[0])**2)+((block[1]-position[1])**2))
            angle = math.atan2(block[1]-position[1], block[0]-position[1])
            relative_angle = angle - robot_angle
            data = [block[0], block[1], distance, relative_angle]
            block_data[blocks.index(block)] = data

        return block_data

    def choose_next_block(self, block_data, reject_blocks):
        """Return the position and relative angle of the next block to navigate to"""
        raise NotImplementedError

    def add_block_to_rejects(self, blocks, position, angle):
        """Detect rejected block when dropped behind robot and record coordinates"""
        raise NotImplementedError


def main():
    blocks = [(1,1), (2,1), (4,7)]
    nav = Navigate()
    nav.calculate_distances_angles(blocks, (0,0), 0)

if __name__ == "__main__":
    main()