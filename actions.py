#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g

def init():
    enable_servos()
    u.move_servo(c.servoArm, c.armUp, 10)
    print("moving arm up")
    u.move_servo(c.servoClaw, c.clawOpen, 10)
    print("opening claw")
    u.move_servo(c.servoWrist, c.wristPipeVertical, 10)
    print("moving wrist horizontal")


def grabCluster():
    print ("Grabbing cluster")
    u.move_servo(c.servoArm, c.armDown, 10)
    g.drive_timed(30, 0.8)  #1
    u.move_servo(c.servoClaw, c.clawClosed, 5)
    msleep(1000)
    u.move_servo(c.servoArm, c.armUp, 20)
    msleep(300)


def driveToMC():
    print ("Driving to medical center")
    g.drive_timed(50, 2.4)
    g.pivot_on_left_wheel(50, 74)   #50, 90
    d.timedLineFollowRight(4.5)




