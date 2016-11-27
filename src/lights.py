__author__ = 'david'
import RPi.GPIO as GPIO

def updateLEDs(grid, x, y, sleep, period):
    x_channel_list = x
    y_channel_list = y
    numx = numy = 0
    for x in grid:
        for y in x:
            GPIO.output(x_channel_list[numx], GPIO.LOW)
            if (y):
                GPIO.output(y_channel_list[numy], GPIO.HIGH)
            if(sleep):
                sleep(period)
            GPIO.output(y_channel_list[numy], GPIO.HIGH)
            numy += 1
        numy =0
        numx +=1

def flashLEDs(grid, x, y, period):
    updateLEDs(grid, x, y, TRUE, period)

def setupLEDs(x, y):
    x_channel_list = x
    y_channel_list = y

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(x_channel_list, GPIO.OUT)
    GPIO.setup(y_channel_list, GPIO.OUT)