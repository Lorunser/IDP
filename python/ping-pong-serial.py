import serial #needed for serial
import time

ArduinoSerial = serial.Serial('com10', 9600) # find right com channel
time.sleep(2) # wait for connection to be established

print(ArduinoSerial.readline()) #read the serial data and print as a line

while 1:
    #send
    message = input("input: ")
    ArduinoSerial.write(str.encode(message))

    #receive
    received = ArduinoSerial.readline()
    print(received)

    time.sleep(1)