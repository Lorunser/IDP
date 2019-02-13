from utils.arduino_connection import Arduino_Connection

def run():
    arduino = Arduino_Connection(com="com9")
    arduino.turn_out_right()

if __name__ == "__main__":
    run()