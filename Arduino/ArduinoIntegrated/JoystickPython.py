import serial
import time

py_serial = serial.Serial(port='COM7', baudrate=9600)

while True:
    if py_serial.readable():

        # Read serial line
        response = py_serial.readline()
        # trun string into list
        response_list = response.split()

        if len(response_list) >= 2:
            print(int(response_list[0]), int(response_list[1]))

            # turn string list into integer
            valX = int(response_list[0])
            valY = int(response_list[1])

            # set trigger values
            trigger_threshold = 100
            if valX >= (500 + trigger_threshold):
                joystick_input = "Right"
                py_serial.write(b"a")   # 적외선 송신
            elif valX <= (500 - trigger_threshold):
                joystick_input = "Left"
            elif valY >= (500 + trigger_threshold):
                joystick_input = "Down"
            elif valY <= (500 - trigger_threshold):
                joystick_input = "Up"
            else:
                joystick_input = "Center"

            print(joystick_input)

            # time.sleep(0.5)   # 딜레이를 아두이노 코드에서 줘야 작동이 됨