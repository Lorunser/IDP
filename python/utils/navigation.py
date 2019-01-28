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
        for block in block_data:
            data = block_data[block]
            if block in reject_blocks:
                score = -1
            else:
                score = 2 * data[2] + 3 * data[3]
            data.append(score)
            block_data[block] = data
            print(score)

        best_block = 0
        best_score = block_data[0][4]
        for block in block_data:
            if 0 < block_data[block][4] < best_score:
                best_block = block
                best_score = block_data[block][4]

        return best_block

    def add_block_to_rejects(self, blocks, position, angle):
        """Detect rejected block when dropped behind robot and record coordinates"""
        raise NotImplementedError


def main():
    blocks = [(1, 1), (2, 1), (4, 7)]
    nav = Navigate()
    block_data = nav.calculate_distances_angles(blocks, (0,0), 0)
    best_block = nav.choose_next_block(block_data, [])
    print(best_block)


if __name__ == "__main__":
    main()