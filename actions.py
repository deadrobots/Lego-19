#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import camera as m

#speed value should be no greater than 1400
#drives lego foreward using ticks
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
    while analog(c.tophat) < 3000
        mav(1000)
        mav(1000)
