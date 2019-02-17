import math


class Navigate:
    """Code for choosing the next block to travel to and return relative angle and distance"""

    def __init__(self):
        self.reject_blocks = []

    def go_to_point(self, position, robot_angle, point):
        """Navigate the robot to a specified point and return true or false as to whether it has arrived"""
        distance = math.sqrt((point[0]-position[0])**2 + (point[1]-position[1])**2)
        if distance > 30:
            if point[0]-position[0] != 0:
                desired_angle = math.atan2((point[1] - position[1]), (point[0] - position[0]))
            #print(point[1]-position[1])
            #print(point[0]-position[0])
                return desired_angle, False
        else:
            return 0, True

    def go_to_corner(self, position, robot_angle):
        """NOT USED"""
        if position[0]>550:
            desired_angle = 1.57
            control(arduino, controller, robot_angle, desired_angle)
            return True
        else:
            if position[1] < 50:
                desired_angle = 0.5
            elif position[1] > 100:
                desired_angle = -0.5
            else:
                desired_angle = 0
            control(arduino, controller, robot_angle, desired_angle)
            return False

    def got_to_line(self, position, robot_angle):
        """NOT USED"""
        if position[1]>200:
            desired_angle = 1.57
            control(arduino, controller, robot_angle, desired_angle)
            return True
        else:
            if position[0] < 500:
                desired_angle = 1
            elif position[0] > 600:
                desired_angle = 2
            else:
                desired_angle = 1.57
            control(arduino, controller, robot_angle, desired_angle)
            return False

    def blocks_left(self, block_data):
        """NOT USED"""
        for block in block_data:
            for reject in self.reject_blocks:
                distance = math.sqrt((block_data[block][0]-reject[0])**2 + (block_data[block][1]-reject[1])**2)
                if distance > 40:
                    return True
                
        return False             


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

    def reject_line(self, block_data):
        """Remove blocks on line from list of blocks as positions already known"""
        for block in block_data:
            if 520<block_data[block][0] and 130<block_data[block][1]<430:
                self.reject_blocks.append((block_data[block][0], block_data[block][1]))
        print(self.reject_blocks)

    def return_rejects(self):
        return self.reject_blocks

    def choose_next_block(self, block_data):
        """Return the position and relative angle of the next block to navigate to"""
        """NOT USED"""
        for block in block_data:
            data = block_data[block]
            score = 0
            for reject in self.reject_blocks:
                if abs(block_data[block][0]-reject[0])<30 and abs(block_data[block][0]-reject[0])<30:
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
        """NOT USED"""
        reject_coords = []
        for block in block_data:
            print(block_data[block][2]<150)
            print(abs(block_data[block][3])>2.5)
            if block_data[block][2]<150 and abs(block_data[block][3])>2.5:
                reject_coords.append((block_data[block][0], block_data[block][1]))
        if reject_coords:
            self.reject_blocks = reject_coords
            return True
        else:
            return False


    def block_in_range(self, best_block, block_data, position, angle):
        """Detect if block is in pickup range"""
        """NOT USED"""
        if block_data[best_block][2]<150 and abs(block_data[best_block][3])<0.6:
            return True
        else:
            return False

#    def dont_crash(self, arg_str_positional, angle):
        # if position beyond range 

def main():
    blocks = [(1, 1), (2, 1), (4, 7)]
    nav = Navigate()
    block_data = nav.calculate_distances_angles(blocks, (0, 0), 0)
    best_block = nav.choose_next_block(block_data)
    #print(nav.add_block_to_rejects(block_data, (0,0), 2.3))
    print(best_block)


if __name__ == "__main__":
    main()
