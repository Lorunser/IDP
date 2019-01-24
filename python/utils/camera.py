import openCV

class Camera:
    """code for handling camera"""


    def __init__(self):
        raise NotImplementedError

    def get_robot_position(self):
        """returns position and angle of robot
        (x_coord, y_coord), angle_in_deg"""
        raise NotImplementedError

    def get_block_coords(self):
        """blah"""
        raise NotImplementedError
