import serial
import time

py_serial = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

while True:
      
    commend = input('press a to send IR signal : ')
    
    py_serial.write(commend.encode())   # encode input and write to arduino
    
    time.sleep(0.1)
    
    if py_serial.readable():
        
        # read from arduino
        response = py_serial.readline()
        print(response[:len(response)-1].decode())