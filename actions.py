#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g

leftBurning = 1


def init():    #align parts with lines on board, pom directly to the right of pom
    if c.isClone:
        print("Hi! I'm Clone.")
    else:
        print("Hi! I'm Prime.")
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
    u.move_servo(c.servoArm, c.armDown, 10)  #grabbing cluster (fireman and water pom)
    g.drive_timed(60, 0.4)  #1
    u.move_servo(c.servoClaw, c.clawClosed, 10)
    msleep(300)
    u.move_servo(c.servoArm, c.armUp, 10)
    msleep(300)
    g.drive_distance(50, 2)
    msleep(300)


def driveToMC():
    print ("Driving to medical center")
    g.pivot_on_left_wheel(75, 90)
    msleep(300)
    d.drive_to_black_and_square_up(60)
    d.drive_to_white_and_square_up(60)
    d.drive_to_black_and_square_up(60)          #squaring up on line next to water block
    g.drive_distance(-50, 3.5)
    msleep(300)
    g.pivot_on_right_wheel(50, 90)      #turn to face silver line
    msleep(500)


def dropOffCluster():
    global leftBurning
    print("Dropping off cluster")
    g.drive_distance(50, 14)  # driving towards silver line (tophats land just past silver line, on black)]\
    d.drive_to_white_and_square_up(70)  # square up on white (past black and silver line)
    if leftBurning == 1:
        if c.isClone:
            g.drive_distance(50, 1)
        else:
            g.drive_distance(50, 1.5)
        g.turn_with_gyro(-50, 50, 90)  # turns and squares up on black
        msleep(100)
        g.drive_distance(50, 6.3) #6.5
    else:
        #g.drive_distance(50, 19)
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
    g.drive_condition(-30, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-30, -30)
    msleep(500)
    # g.drive_distance(30, 1)
    msleep(100)
    u.move_servo(c.servoArm, c.armDropOff, 5)   #drops off cluster
    msleep(250)
    u.move_servo(c.servoClaw, c.clawOpen, 3)
    msleep(250)
    u.move_servo(c.servoArm, c.armUp, 3)
    msleep(100)
    if c.isClone:
        if leftBurning == 1:
            g.drive_distance(30, 1)
    else:
        g.drive_distance(30, 1)


def driveToFiretruck():
    global leftBurning
    print("Driving to firetruck")
    d.drive_to_black_and_square_up(-60)   #squares up on black
    if c.isClone:
        g.drive_distance(50, 6.0)
    else:
        if leftBurning == 1:
            g.drive_distance(50, 3.5)
        else:
            g.drive_distance(50, 5.5)
    #g.turn_with_gyro(-50, 50, 90)
    if leftBurning == 1:
        g.pivot_on_left_wheel(50, 87)   #turns and drives forward to square up on black line
    else:
        g.pivot_on_left_wheel(50, 90)
    msleep(100)
    g.drive_distance(-50, 4)
    msleep(500)
    if leftBurning == 1:    #switched code from else to left
        print("left burning routine")
        d.drive_to_black_and_square_up(70)  #squares up
        msleep(500)
    else:
        print("right burning routine")
        d.drive_to_black_and_square_up(70)
        d.drive_to_white_and_square_up(70)
        #g.drive_distance(50, 20)
        g.drive_distance(50, 4)
        msleep(500)
        d.drive_to_black_and_square_up(70) #True #drives until the black line at the end of the medical center


def pickUpFiretruck():
    global leftBurning
    print("Picking up firetruck")
    d.drive_to_white_and_square_up(70)
    msleep(500)
    if c.isClone:
        g.turn_with_gyro(-30, 30, 10)
    else:
        # g.turn_with_gyro(-30, 30, 10)
        pass
    msleep(250)
    if c.isClone:
        g.drive_distance(-50, 1)
    else:
        g.drive_distance(-50, 2.5)
    u.move_servo(c.servoArm, c.armDown, 10)
    msleep(250)
    if c.isClone:
        pass
    else:
        g.drive_distance(25, 1.5)
    u.move_servo(c.servoClaw, c.clawClosed, 5)
    msleep(250)
    u.move_servo(c.servoArm, c.armUp, 5)
    msleep(250)


def dropOffFiretruck():
    global leftBurning
    if leftBurning == 1:
        if c.isClone:
            g.turn_with_gyro(30, -30, 10)
            msleep(250)
            g.drive_distance(70, 2)
            d.drive_to_black_and_square_up(70)
            u.waitForButton()
            g.drive_distance(-50, 2)
            msleep(250)
            d.drive_to_black_and_square_up(-70)
            msleep(250)
            g.turn_with_gyro(50, -50, 90)
            u.waitForButton()
            msleep(500)
            d.drive_till_black_right(-70)
            u.waitForButton()
            g.drive_distance(-70, 4)
            u.waitForButton()
            u.move_servo(c.servoArm, c.armDown, 5)  #delivering firetruck
            u.waitForButton()
            u.move_servo(c.servoClaw, c.clawOpen, 3)
            u.waitForButton()
            u.move_servo(c.servoArm, c.armUp, 3)
        else:
            g.drive_distance(50, 11)
            g.turn_with_gyro(-50, 50, 180)
            u.move_servo(c.servoArm, c.armDown, 5)  # delivering firetruck
            u.move_servo(c.servoClaw, c.clawOpen, 3)
            u.move_servo(c.servoArm, c.armUp, 3)
    else:
        if c.isClone:
            pass
        else:
            g.turn_with_gyro(-50, 50, 180)
            msleep(600)
            g.drive_distance(50, 1)
            u.move_servo(c.servoArm, c.armDown, 5)  # delivering firetruck
            u.move_servo(c.servoClaw, c.clawOpen, 3)
            u.move_servo(c.servoArm, c.armUp, 3)

    #Sunday to do: take out wait for buttons above, increase the speed of the drop off (and over all run)
    #code for drop off of firetruck in right burning medical center
    #if time, begin working on gas valve delivery (no longer doing firemen due to time and point oppotunities with both gas valves)
