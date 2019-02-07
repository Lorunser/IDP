from utils.arduino_connection import Arduino_Connection
from utils.arduino_connection import Block_States
import time

def run():
    arduino = Arduino_Connection(com="com9")

    while(True):
        block_state = arduino.get_block_state()
        print(block_state)
        time.sleep(1)


if __name__ == "__main__":
    run()