#!/usr/bin/python
from wallaby import *
import wallaby as w  #pick one convention eventually
import utils as u
import constants as c


def driveTimed(left, right, time):
    motor(c.LMOTOR, left)
    motor(c.RMOTOR, right)
    msleep(time)
    ao()

def sleep(time):
    driveTimed(0, 0, time)

def drive(left, right):
    motor(c.LMOTOR,left)
    motor(c.RMOTOR,right)

def lineFollowLeft(time):
    sec = seconds()
    while(seconds()-sec<time):
        if(u.onBlackFront()):
            drive(40,70)#was 45
        else:
            drive(70,40)#was 45
    drive(0,0)

def lineFollowRight(time):
    sec = seconds()
    while(seconds()-sec<time):
        if(u.onBlackFront()):
            drive(60,55)
        else:
            drive(55,60)
    drive(0,0)


def tickDrive(time, speed1, speed2):
    if speed1 > 1400:
        print("speed too fast. please pick a number under 1401.")
        speed1 = 1400
    if speed1 > 1400:  # You are checking for "edge-cases" here. This is solid coding. Well done! - LMB
        print("speed too fast. please pick a number under 1401.")
        speed2 = 1400
    mav(c.motorLeft, speed1)
    mav(c.motorRight, speed2)
    msleep(time)


def driveTillBlack():
    while analog(c.tophat) < 3000:
        mav(1000)
        mav(1000)

# Loop break timers #

time = 0  # This represents how long to wait before breaking a loop.


def setWait(DELAY):  # Sets wait time in seconds before breaking a loop.
    global time
    time = seconds() + DELAY


def getWait():  # Used to break a loop after using "setWait". An example would be: setWiat(10) | while true and getWait(): do something().
    return seconds() < time


def onBlackFront():
    return w.analog(c.FRONT_TOPHAT) > c.onBlack


def timedLineFollowLeft(time):
    sec = seconds() + time
    while seconds() < sec:
        if onBlackFront():
            driveTimed(20, 90, 20)
        else:
            driveTimed(90, 20, 20)
        msleep(10)


# Follows black line on right for specified amount of time
def timedLineFollowRight(time):
    sec = seconds() + time
    while seconds() < sec:
        if not onBlackFront():
            driveTimed(20, 90, 20)
        else:
            driveTimed(90, 20, 20)
        msleep(10)


def timedLineFollowRightSmooth(time):
    sec = seconds() + time
    while seconds() < sec:
        if not onBlackFront():
            driveTimed(20, 40, 20)
        else:
            driveTimed(40, 20, 20)
        msleep(10)


def lineFollowRightSmoothCount(amount):
    count = 0
    while count < amount:
        if not onBlackFront():
            driveTimed(10, 30, 10)
            count = count + 1
        else:
            driveTimed(30, 10, 10)
            count = 0


def timedLineFollowLeftSmooth(time):
    sec = seconds() + time
    while seconds() < sec:
        if onBlackFront():
            driveTimed(20, 40, 20)
        else:
            driveTimed(40, 20, 20)
        msleep(10)


def timedLineFollowLeftBack(time):  # follows on starboard side
    sec = seconds() + time
    while seconds() < sec:
        if onBlackBack():
            driveTimed(-90, -20, 20)
        else:
            driveTimed(-20, -90, 20)
        msleep(10)


def crossBlackFront():
    while not onBlackFront():  # wait for black
        pass
    while onBlackFront():  # wait for white
        pass
    ao()


def crossBlackBack():
    while not onBlackBack():  # wait for black
        pass
    while onBlackBack():  # wait for white
        pass
    ao()
