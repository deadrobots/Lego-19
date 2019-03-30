#!/usr/bin/python
from wallaby import *
import constants as c


def driveTimed(left, right, time):
    motor(c.LEFT_MOTOR, left)
    motor(c.RIGHT_MOTOR, right)
    msleep(time)
    ao()

def waitForButton():
    print("Press Right Button...")
    while not digital(c.RIGHT_BUTTON):
        pass
    msleep(1)
    print("Pressed")
    msleep(1000)

def DEBUG():
    freeze(c.LEFT_MOTOR)
    freeze(c.RIGHT_MOTOR)
    print('Program stop for DEBUG\nSeconds: ', seconds() - c.start_time)
    ao()
    exit(0)

def DEBUGwithWait():
    freeze(c.LEFT_MOTOR)
    freeze(c.RIGHT_MOTOR)
    print ('Program stop for DEBUG\nSeconds: ', seconds() - c.start_time)
    ao()
    msleep(5000)

def sleep(time):
    driveTimed(0, 0, time)

def drive(left, right):
    motor(c.LEFT_MOTOR, left)
    motor(c.RIGHT_MOTOR, right)

######################################
def wait_4_light(ignore=False):
    if ignore:
        waitForButton()
        return
    while not calibrate(c.START_LIGHT):
        pass
    _wait_4(c.START_LIGHT)


def calibrate(port):
    print("Press LEFT button with light on")
    while not left_button():
        pass
    while left_button():
        pass
    lightOn = analog(port)
    print("On value =", lightOn)
    if lightOn > 200:
        print("Bad calibration")
        return False
    msleep(1000)
    print("Press RIGHT button with light off")
    while not right_button():
        pass
    while right_button():
        pass
    lightOff = analog(port)
    print("Off value =", lightOff)
    if lightOff < 3000:
        print("Bad calibration")
        return False

    if (lightOff - lightOn) < 2000:
        print("Bad calibration")
        return False
    c.startLightThresh = (lightOff - lightOn) / 2
    print("Good calibration! ", c.startLightThresh)
    return True


def _wait_4(port):
    print("waiting for light!! ")
    while analog(port) > c.startLightThresh:
        pass
#####################################

def move_servo(servo, endPos, speed=10):
    now = get_servo_position(servo)
    if now > 2047:
        print("Servo setting too large ", servo)
    if now < 0:
        print("Servo setting too small ", servo)
    if now > endPos:
        speed = -speed
    for i in range(now, endPos, speed):
        set_servo_position(servo, i)
        msleep(10)
    set_servo_position(servo, endPos)
    msleep(10)

