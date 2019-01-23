import serial #needed for serial
import time


def run():
    ArduinoSerial = serial.Serial('com11', 9600) # find right com channel
    time.sleep(2) # wait for connection to be established

    #print(ArduinoSerial.readline()) #read the serial data and print as a line

    while 1:
        #send
        message = input("input: ")
        ArduinoSerial.write(str.encode(message))

        #receive
        received = receiveLine(ArduinoSerial)
        print(received)

        #time.sleep(1)


def receiveLine(serialConnection):
    message = serialConnection.readline()
    message = str(message.decode('ASCII'))
    message = message[0:-2]
    return message


if __name__ == "__main__":
    run()
