__author__ = 'david'
import RPi.GPIO as GPIO
import time


def updateLEDs(grid, x, y):
    x_channel_list = x
    y_channel_list = y
    numx = numy = 0
    for x in grid:
        for y in x:
            if (y):
                GPIO.output(x_channel_list[numx], GPIO.HIGH)
                GPIO.output(y_channel_list[numy], GPIO.LOW)
                time.sleep(0.00005)
            GPIO.output(y_channel_list[numy], GPIO.HIGH)
            GPIO.output(x_channel_list[numx], GPIO.LOW)
            numy += 1
        numy =0
        numx +=1

def setupLEDs(x, y):
    x_channel_list = x
    y_channel_list = y

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(x_channel_list, GPIO.OUT)
    GPIO.setup(y_channel_list, GPIO.OUT)