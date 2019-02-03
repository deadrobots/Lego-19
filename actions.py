#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g

leftBurning = 0


def init():
    enable_servos()
    g.calibrate_gyro()
    msleep(250)
    u.move_servo(c.servoArm, c.armDown, 5)
    print("Moving arm down")
    u.move_servo(c.servoArm, c.armUp, 10)
    print("moving arm up")
    u.move_servo(c.servoClaw, c.clawOpen, 10)
    print("opening claw")
    u.move_servo(c.servoWrist, c.wristPipeVertical, 10)
    print("moving wrist horizontal")


def grabCluster():
    global leftBurning
    done = seconds() + 5.0
    while seconds() < done:
        if digital(c.BUTTON) == 1:
            leftBurning = 1
            print("The burning medical center is on the left")
        print("waiting for create")
        msleep(10)
    print ("Grabbing cluster")
    u.move_servo(c.servoArm, c.armDown, 5)
    g.drive_timed(30, 0.8)  #1
    u.move_servo(c.servoClaw, c.clawClosed, 5)
    msleep(1000)
    u.move_servo(c.servoArm, c.armUp, 5)
    msleep(300)
    g.drive_distance(50, 2)
    msleep(300)



def driveToMC():
    print ("Driving to medical center")
    g.pivot_on_left_wheel(50, 90)
    msleep(500)
    g.drive_condition(70, d.on_black_right or d.on_black_left, False)
    d.square_up_black(50, 50)
    msleep(500)
    g.drive_condition(70, d.on_black_right or d.on_black_left, True)
    d.square_up_white(50, 50)
    msleep(500)
    g.drive_condition(70, d.on_black_right or d.on_black_left, False)
    d.square_up_black(50, 50)
    msleep(500)
    g.drive_condition(70, d.on_black_right or d.on_black_left, True)
    d.square_up_white(50, 50)
    msleep(500)
    g.pivot_on_right_wheel(50, 93)
    msleep(500)


def dropOffCluster():
    global leftBurning
    print("Dropping off cluster")
    if leftBurning == 1:
        g.drive_distance(50, 19)
        msleep(250)
    else:
        g.drive_distance(50, 19)
        d.timedLineFollowRightSmooth(6.3)
        msleep(250)
    u.waitForButton()
    g.turn_with_gyro(-50, 50, 90)
    msleep(100)
    g.drive_condition(-30, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-30, -30)
    msleep(500)
    g.drive_distance(30, 1)
    msleep(100)
    u.move_servo(c.servoArm, c.armDropOff, 5)
    msleep(250)
    u.move_servo(c.servoClaw, c.clawOpen, 5)
    msleep(250)
    u.move_servo(c.servoArm, c.armUp, 10)
    msleep(100)


def driveToFiremen():
    global leftBurning
    print("Driving to firemen")
    g.drive_condition(-30, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-30, -30)
    msleep(500)
    g.drive_distance(50, 6)
    #g.turn_with_gyro(-50, 50, 90)
    g.pivot_on_left_wheel(50, 87)
    msleep(100)
    u.waitForButton()
    if leftBurning == 1:
        #g.drive_distance(50, 10)
        g.drive_condition(70, d.on_black_right or d.on_black_left, True)
        d.square_up_black(50, 50)
        msleep(500)
    else:
        g.drive_distance(50, 3)
        g.drive_condition(70, d.on_black_right or d.on_black_left, True)
        d.square_up_black(50, 50)
        msleep(500)
        #g.drive_distance(50, 20)
    u.waitForButton()
    g.drive_distance(50, 4)
    g.drive_condition(70, d.on_black_right or d.on_black_left, True)
    d.square_up_black(50, 50)
    msleep(500)


def dropOffFiremen():
    global leftBurning
    print("Dropping off firemen")



