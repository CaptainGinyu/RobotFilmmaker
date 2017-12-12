import serial

arduinoSerial = serial.Serial('/dev/ttyACM0', 9600)

while True:
    arduinoSerial.write(bytes(input('Enter first angle, then a comma, then second angle: '), 'UTF-8'))
