import serial
import time


class Arduino_Connection:
    """Wrapper class for handling connection methods"""


    def __init__(self, com="com9", baud_rate=9600):
        self.serial_connection = serial.Serial(com, 9600)
        time.sleep(2)
        print("Connection Established")


    def receive_line(self):
        """Attempts to read a line from serial"""
        try:
            message = self.serial_connection.readline()
            message = str(message.decode('ASCII'))
            message = message[0:-2]
            return message
        except:
            raise ConnectionError("Nothing to receive")


    def send_line(self, message):
        """Send given message over serial"""
        self.serial_connection.write(str.encode(message))

    
    def drive(self, direction, pace, debug=False):
        """Send appropriate motor controls after checking"""
        
        # enforce limits on direction and pace (-1) <-> (1)
        if (abs(direction) > 1):
            direction = int(direction / abs(direction))
        
        if (abs(pace) > 1):
            pace = int(pace / abs(pace))

        command = str(round(direction, 3)) + "," + str(round(pace, 3))
        print(command)
        self.send_line(command)


    
