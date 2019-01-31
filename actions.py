#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d

def init():
    enable_servos()
    u.move_servo(c.servoArm, c.armUp, 10)
    print("moving arm up")
    u.move_servo(c.servoClaw, c.clawOpen, 10)
    print("opening claw")
    u.move_servo(c.servoWrist, c.wristPipeVertical, 10)
    print("moving wrist horizontal")


def grabCluster():
    u.move_servo(c.servoArm, c.armDown, 10)
    d.driveTimed(30, 30, 1000)
    u.move_servo(c.servoClaw, c.clawClosed, 5)
    msleep(2000)
    u.move_servo(c.servoArm, c.armUp, 20)
    msleep(300)

def driveToMC():
    d.driveTimed(50, 50, 2000)
