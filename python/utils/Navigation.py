class Navigate:
    """Code for choosing the next block to travel to and return relative angle and distance"""

    def __init__(self):
        raise NotImplementedError

    def calculate_distances_angles(self, blocks, position, angle):
        """Return array of distances and relative angles"""
        raise NotImplementedError

    def choose_next_block(self, block_data, reject_blocks):
        """Return the position and relative angle of the next block to navigate to"""
        raise NotImplementedError

    def add_block_to_rejects(self, blocks, position, angle):
        """Detect rejected block when dropped behind robot and record coordinates"""
        raise NotImplementedError