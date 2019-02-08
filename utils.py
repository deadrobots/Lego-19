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
    print('Program stop for DEBUG\nSeconds: ', seconds() - c.startTime)
    ao()
    exit(0)

def DEBUGwithWait():
    freeze(c.LEFT_MOTOR)
    freeze(c.RIGHT_MOTOR)
    print ('Program stop for DEBUG\nSeconds: ', seconds() - c.startTime)
    ao()
    msleep(5000)

def sleep(time):
    driveTimed(0, 0, time)

def drive(left, right):
    motor(c.LEFT_MOTOR, left)
    motor(c.RIGHT_MOTOR, right)

# def lineFollowLeft(time):
#     sec = seconds()
#     while(seconds()-sec<time):
#         if(u.onBlackFront()):
#             drive(40,70)#was 45
#         else:
#             drive(70,40)#was 45
#     drive(0,0)
#
# def lineFollowRight(time):
#     sec = seconds()
#     while(seconds()-sec<time):
#         if(u.onBlackFront()):
#             drive(60,55)
#         else:
#             drive(55,60)
#     drive(0,0)

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

