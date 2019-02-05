import serial
import time
from enum import Enum

class Block_States(Enum):
    """Classify data recived from Arduino"""
    NO_BLOCK = 0
    BLOCK_DETECTED = 1
    BLOCK_ACCEPTED = 2
    BLOCK_REJECTED = 3

class Arduino_Connection:
    """Wrapper class for handling connection methods"""

    def __init__(self, com="com9", baud_rate=9600):
        self.serial_connection = serial.Serial(com, 9600)
        time.sleep(2)
        print("Connection Established")


    def receive_line(self):
        """Attempts to read a line from serial"""
        if (serial_connection.inWaiting()):
            message = self.serial_connection.readline()
            message = str(message.decode('ASCII'))
            message = message[0:-2]
            return message
        return "0"


    def get_block_state(self):
        message = receive_line()
        code = int(message)

        block_state = Block_States()
        block_state.value = code
        return block_state

    def send_line(self, message):
        """Send given message over serial"""
        #append terminator '&'
        message = message + '&'
        self.serial_connection.write(message.encode('ASCII'))

    
    def drive(self, direction, pace, debug=False):
        """Send appropriate motor controls after checking"""
        
        # enforce limits on direction and pace (-1) <-> (1)
        if (abs(direction) > 1):
            direction = int(direction / abs(direction))
        
        if (abs(pace) > 1):
            pace = int(pace / abs(pace))

        command = str(round(direction, 3)) + "," + str(round(pace, 3))
        
        if (debug):
            print(command)
            
        self.send_line(command)


    
