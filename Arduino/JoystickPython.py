import serial
import time

py_serial = serial.Serial(port='/dev/ttyACM0', baudrate=9600)

while True:
    if py_serial.readable():
        
        # Read serial line
        response = py_serial.readline()
        
        # trun string into list
        response_list = response.split()
        print(int(response_list[0]), int(response_list[1]))
        
        # turn string list into integer
        valX = int(response_list[0])
        valY = int(response_list[1])
        
        # set trigger values
        trigger_threshold = 100
        if valX >= (500 + trigger_threshold):
            input_ = "Right"
        elif valX <= (500 - trigger_threshold):
            input_ = "Left"
        elif valY >= (500 + trigger_threshold):
            input_ = "Down"
        elif valY <= (500 - trigger_threshold):
            input_ = "Up"
        else:
            input_ = "Center"
        
        print(input_)


