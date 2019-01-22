import serial #needed for serial
import time


def run():
    ArduinoSerial = serial.Serial('com11', 115200) # find right com channel
    time.sleep(2) # wait for connection to be established

    print(ArduinoSerial.readline()) #read the serial data and print as a line

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
    message = str(message.decode('utf-8'))
    message = message.replace('\r\n', '')
    return message


if __name__ == "__main__":
    run()
