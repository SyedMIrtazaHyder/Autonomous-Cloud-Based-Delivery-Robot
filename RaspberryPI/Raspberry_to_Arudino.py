import time
import RPi.GPIO as gpio
import math

threshold = 500

dig_A = 11
dig_B = 13
dig_X = 15


left_PWM = 33
right_PWM = 32

gpio.setwarnings(False)
gpio.cleanup()

print("Setting Up")
gpio.setmode(gpio.BOARD)
gpio.setup(dig_A, gpio.OUT)
gpio.setup(dig_B, gpio.OUT)
gpio.setup(dig_X, gpio.OUT)

gpio.setup(left_PWM, gpio.OUT)
gpio.setup(right_PWM, gpio.OUT)

speed_left = gpio.PWM(left_PWM, 1000)
speed_right = gpio.PWM(right_PWM, 1000)
speed_left.start(100)
speed_right.start(100)

delay = 5

def stop():
    global delay
    gpio.output(dig_X, gpio.HIGH)
    time.sleep(delay)

def straight():
    global delay
    gpio.output(dig_A, gpio.LOW)
    gpio.output(dig_B, gpio.LOW)
    gpio.output(dig_X, gpio.LOW)
    time.sleep(delay)

def left():
    global delay
    gpio.output(dig_A, gpio.HIGH)
    gpio.output(dig_B, gpio.LOW)
    gpio.output(dig_X, gpio.LOW)
    time.sleep(delay)

def right():
    global delay
    gpio.output(dig_A, gpio.LOW)
    gpio.output(dig_B, gpio.HIGH)
    gpio.output(dig_X, gpio.LOW)
    time.sleep(delay)

def back():
    global delay
    gpio.output(dig_A, gpio.HIGH)
    gpio.output(dig_B, gpio.HIGH)
    gpio.output(dig_X, gpio.LOW)
    time.sleep(delay)
