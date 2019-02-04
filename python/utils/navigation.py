import math


class Navigate:
    """Code for choosing the next block to travel to and return relative angle and distance"""

    def __init__(self):
        self.reject_blocks = []

    def got_to_corner(self, position, robot_angle):


    def calculate_distances_angles(self, blocks, position, robot_angle):
        """Return array of distances and relative angles"""
        block_data = {}
        data = []
        for block in blocks:
            # data = [block[0], block[1]]
            distance = math.sqrt(((block[0] - position[0]) ** 2) + ((block[1] - position[1]) ** 2))
            angle = math.atan2(block[1] - position[1], block[0] - position[0])
            relative_angle = angle - robot_angle
            data = [block[0], block[1], distance, relative_angle]
            block_data[blocks.index(block)] = data

        return block_data

    def choose_next_block(self, block_data):
        """Return the position and relative angle of the next block to navigate to"""
        for block in block_data:
            data = block_data[block]
            score = 0
            for reject in self.reject_blocks:
                if abs(block_data[block][0]-reject[0])<50 and abs(block_data[block][0]-reject[0])<50:
                    score = -1
            if score != -1:
                score = 2 * data[2] + 3 * data[3]
            data.append(score)
            block_data[block] = data
            #print(score)

        best_block = 0
        best_score = block_data[0][4]
        for block in block_data:
            if 0 < block_data[block][4] < best_score:
                best_block = block
                best_score = block_data[block][4]

        return best_block

    def add_block_to_rejects(self, block_data, position, angle):
        """Detect rejected block when dropped behind robot and record coordinates"""
        reject_coords = []
        for block in block_data:
            if block_data[block][2]<150 and abs(block_data[block][3])>2.5:
                reject_coords.append((block_data[block][0], block_data[block][1]))
        if reject_coords:
            self.reject_blocks = reject_coords
            return True
        else:
            return False


    def block_in_range(self, best_block, block_data, position, angle):
        """Detect if block is in pickup range"""
        if block_data[best_block][2]<150 and abs(block_data[best_block][3])<0.6:
            return True
        else:
            return False

def main():
    blocks = [(1, 1), (2, 1), (4, 7)]
    nav = Navigate()
    block_data = nav.calculate_distances_angles(blocks, (0, 0), 0)
    best_block = nav.choose_next_block(block_data)
    #print(nav.add_block_to_rejects(block_data, (0,0), 2.3))
    print(best_block)


if __name__ == "__main__":
    main()
