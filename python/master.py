import serial #needed for serial
import time

ArduinoSerial = serial.Serial('com10', 9600) # find right com channel
time.sleep(2) # wait for connection to be established

print(ArduinoSerial.readline()) #read the serial data and print as a line
print("1 to turn ON LED and 0 to turn OFF")

while 1:
    var = input("input: ")

    if (var == '1'):
        ArduinoSerial.write(str.encode('1'))
        print ('LED ON')

    elif (var == '0'):
        ArduinoSerial.write(str.encode('0'))
        print('LED OFF')

    time.sleep(1)