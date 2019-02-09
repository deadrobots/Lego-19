#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g

leftBurning = 0


def init():                 #aligh parts with lines on board, pom directly to the right of pom
    enable_servos()
    g.drive_condition(50, d.on_black_left, False)
    msleep(500)
    g.drive_condition(50, d.on_silver_right, True)
    msleep(500)
    u.move_servo(c.servoClaw, c.clawOpen, 10)
    print("opening claw")
    u.move_servo(c.servoArm, c.armDown, 5)
    print("Moving arm down")
    u.move_servo(c.servoArm, c.armUp, 10)
    print("moving arm up")
    u.move_servo(c.servoWrist, c.wristPipeVertical, 10)
    print("moving wrist horizontal")


def grabCluster():
    global leftBurning
    done = seconds() + 5.0
    while seconds() < done:
        if digital(c.BUTTON) == 1:
            leftBurning = 1
            print("The burning medical center is on the left")
        print("waiting for create")        #waiting for Create to send MC order (which building is on fire)
        msleep(10)
    print ("Grabbing cluster")
    u.move_servo(c.servoArm, c.armDown, 5)          #grabbing cluster (fireman and water pom)
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
    d.drive_to_black_and_square_up(40)
    d.drive_to_white_and_square_up(40)
    d.drive_to_black_and_square_up(40)          #squaring up on line next to water block
    g.drive_distance(-50, 3.5)
    msleep(500)
    g.pivot_on_right_wheel(50, 90)      #turn to face silver line
    msleep(500)


def dropOffCluster():
    global leftBurning
    print("Dropping off cluster")
    if leftBurning == 1:
        g.drive_distance(50, 19)
        msleep(250)
    else:
        #g.drive_distance(50, 19)
        g.drive_distance(50, 15)         #driving towards silver line (tophats land just past silver line, on black)
        d.drive_to_white_and_square_up(70)    #square up on white (past black and silver line)
        g.turn_with_gyro(0, 50, 60)         #wiggles to black line
        msleep(500)
        g.drive_distance(30, 3)
        msleep(250)
        g.turn_with_gyro(50, 0, 60)
        msleep(500)
        d.timedLineFollowRightSmooth(4.4)       #line follows until there is almost no space between it and the pipe
        msleep(250)
    g.turn_with_gyro(-50, 50, 90)           #turns and squares up on black
    msleep(100)
    # d.drive_to_white_and_square_up(30)
    g.drive_condition(-30, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-30, -30)
    msleep(500)
    g.drive_distance(30, 1)
    msleep(100)
    u.move_servo(c.servoArm, c.armDropOff, 5)       #drops off cluster
    msleep(250)
    u.move_servo(c.servoClaw, c.clawOpen, 5)
    msleep(250)
    u.move_servo(c.servoArm, c.armUp, 10)
    msleep(100)


def driveToFiremen():
    global leftBurning
    print("Driving to firemen")
    d.drive_to_black_and_square_up(-30)   #squares up on black
    g.drive_distance(50, 6)
    #g.turn_with_gyro(-50, 50, 90)
    g.pivot_on_left_wheel(50, 85)           #turns and drives forward to square up on black line
    msleep(100)
    u.waitForButton()
    g.drive_distance(-50, 2)
    msleep(500)
    if leftBurning == 1:       #switched code from else to left
        g.drive_distance(50, 3)
        d.drive_to_black_and_square_up(70)
        u.waitForButton()
        d.drive_to_white_and_square_up(70)       #squares up
    else:
        d.drive_to_black_and_square_up(70)
        d.drive_to_white_and_square_up(70)
        #g.drive_distance(50, 20)
    u.waitForButton()
    g.drive_distance(50, 4)
    msleep(500)
    d.drive_to_black_and_square_up(-70) #True #drives until the black line at the end of the medical center
                                                         #complexes then squares up

def dropOffFiremen():
    global leftBurning
    print("Dropping off firemen")



