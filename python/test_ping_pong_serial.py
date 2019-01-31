import time
from utils.arduino_connection import Arduino_Connection


def run():
    arduino = Arduino_Connection(com='com9', baud_rate='9600')

    while 1:
        #send
        message = input("input: ")
        arduino.send_line(message)

        #receive
        #received = arduino.receive_line()
        #print(received)


if __name__ == "__main__":
    run()
