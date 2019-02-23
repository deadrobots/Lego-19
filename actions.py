#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g

leftBurning = 1


def init():   #Clone ---> #align parts with lines on board, pom directly to the right of pom
    #Prime Setup: (The right one)
    #The square up surface on the back of the bot should be flush to the back of the SB
    #The left edge of the square up surface should be just to the left of the coupler
    #I know. This puts LEGO and Create very close, but its necessary. :)
    #
    #^^^^ This setup needs to be fixed on clone
    if c.isClone:
        print("Hi! I'm Clone.")
    else:
        print("Hi! I'm Prime.")
    enable_servos()
    msleep(500)
    print("Don't touch me, I'm calibrating!!!")
    g.calibrate_gyro()
    msleep(500)
    u.move_servo(c.servoArm, c.armDropOff, 10)
    # test the motors
    d.driveTimed(50, 50, 1000)
    d.driveTimed(50, 0, 1000)
    d.driveTimed(-50, 0, 1000)
    print("testing wrist")
    u.move_servo(c.servoWrist, c.wristVertical)
    u.move_servo(c.servoWrist, c.wristHorizontal)
    print("testing claw")
    u.move_servo(c.servoClaw, c.clawClosed)
    u.move_servo(c.servoClaw, c.clawOpen)
    print("testing tophat")
    g.drive_condition(50, d.on_black_left, False)
    g.drive_condition(50, d.on_silver_right, True)
    d.drive_to_white_and_square_up(50)
    print("testing arm")
    u.move_servo(c.servoArm, c.armUp, 10)
    u.move_servo(c.servoArm, c.armDown, 5)
    print("place in start posistion")
    u.waitForButton()
    g.calibrate_gyro()

def grabCluster():
    global leftBurning
    print("Waiting for something to press button")
    done = seconds() + 5.0
    while seconds() < done:  #waiting for Create to send MC order (which building is on fire)
        if digital(c.BUTTON) == 1:
            leftBurning = 0
        msleep(10)
    if leftBurning == 1:
        print("The burning medical center is on the left")
    else:
        print("The burning medical center is on the right")
    print ("Grabbing cluster")
    #u.move_servo(c.servoArm, c.armDown, 10)  #grabbing cluster (fireman and water pom)
    g.drive_timed(60, 0.55)  #0.4
    u.move_servo(c.servoClaw, c.clawClosed, 10)
    msleep(300)
    u.move_servo(c.servoArm, c.armUp, 10)
    msleep(300)
    g.drive_distance(50, 2)

def driveToMC():
    print ("Driving to medical center")
    g.pivot_on_left_wheel(75, 90)
    d.drive_to_black_and_square_up(70)
    d.drive_to_white_and_square_up(70)
    d.drive_to_black_and_square_up(70)          #squaring up on line next to water block
    g.drive_distance(-60, 3.5)
    g.pivot_on_right_wheel(50, 90) #turn to face silver line

def dropOffCluster():
    global leftBurning
    print("Dropping off cluster")
    g.drive_distance(70, 14)  # driving towards silver line (tophats land just past silver line, on black)]\
    d.drive_to_white_and_square_up(70)  # square up on white (past black and silver line)
    if leftBurning == 1:
        if c.isClone:
            g.drive_distance(60, 2)
        else:
            g.drive_distance(50, 2)  #3 (shortened because the delivery was too close to the edge)
        g.turn_with_gyro(-50, 50, 90)  # turns and squares up on black
        g.drive_distance(50, 4) #6.3
    else:
        #g.drive_distance(50, 19)
        g.turn_with_gyro(0, 50, 60)         #wiggles to black line
        g.drive_distance(30, 3)
        g.turn_with_gyro(50, 0, 60)
        d.timedLineFollowRightSmooth(4.4) #line follows until there is almost no space between it and the pipe
        msleep(250)
        g.turn_with_gyro(-50, 50, 90)           #turns and squares up on black
        msleep(100)
    g.drive_condition(-30, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-30, -30)
    msleep(500)
    if c.isPrime:
        g.drive_distance(30, 1) #1
    else:
        g.drive_distance(30, 0.5)  # 1
    u.move_servo(c.servoArm, c.armDropOff, 5)   #drops off cluster
    msleep(250)
    u.move_servo(c.servoClaw, c.clawOpen, 3)
    msleep(250)
    u.move_servo(c.servoArm, c.armUp, 3)
    print ("Delivered!")
    msleep(100)
    if c.isClone:
        if leftBurning == 1:
            g.drive_distance(40, 1)
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
        g.pivot_on_left_wheel(50, 90)   #turns and drives forward to square up on black line #was 87
    else:
        g.pivot_on_left_wheel(50, 90)
    g.drive_distance(-50, 4)
    if leftBurning == 1:                #switched code from else to left
        print("left burning routine")
        d.drive_to_black_and_square_up(70)
        msleep(500)
    else:
        print("right burning routine")
        d.drive_to_black_and_square_up(70)
        d.drive_to_white_and_square_up(70)
        #g.drive_distance(50, 20)
        g.drive_distance(50, 4)
        d.drive_to_black_and_square_up(70) #True #drives until the black line at the end of the medical center


def pickUpFiretruck():
    global leftBurning
    print("Picking up firetruck")
    d.drive_to_white_and_square_up(70)
    msleep(500)
    if c.isClone:
        g.turn_with_gyro(-25, 25, 10)
    else:
        g.turn_with_gyro(-30, 30, 5)
        pass
    msleep(250)
    if c.isClone:
        g.drive_distance(-50, 0.75) #1
    else:
        g.drive_distance(-50, 2.5)
    u.move_servo(c.servoArm, c.armDown, 10)
    msleep(250)
    if c.isClone:
        pass
    else:
        g.drive_distance(25, 2.5)
    u.move_servo(c.servoClaw, c.clawClosed, 7)
    msleep(100)
    u.move_servo(c.servoArm, c.armUp, 7)        #picks up firetruck
    msleep(100)


def dropOffFiretruck():
    print ("drop off firetruck")
    global leftBurning
    if leftBurning == 1:
        if c.isClone:
            g.turn_with_gyro(20, -20, 10)           #correcting turn to pick up firetruck
            d.drive_to_white_and_square_up(70)
            msleep(250)
            g.turn_with_gyro(50, -50, 90)
            d.drive_till_black_right(-70)
            g.drive_distance(-70, 3) #was 4
            u.move_servo(c.servoArm, c.armDown, 5)  #delivering firetruck
            msleep(100)
            u.move_servo(c.servoClaw, c.clawOpen, 6)
            msleep(100)
            msleep(100)
            u.move_servo(c.servoArm, c.armUp, 6)
        else:
            #This is a copy and paste of the current strategy for clone, but it doesn't work (at all)
            #Please work to make these firetruck pick up and drop offs more consistent for P + C
            d.drive_to_white_and_square_up(70)
            msleep(250)
            g.turn_with_gyro(50, -50, 90)
            d.drive_till_black_right(-70)
            g.drive_distance(-70, 3)  # was 4
            u.move_servo(c.servoArm, c.armDown, 5)  # delivering firetruck
            msleep(100)
            u.move_servo(c.servoClaw, c.clawOpen, 6)
            msleep(100)
            msleep(100)
            u.move_servo(c.servoArm, c.armUp, 6)
           # g.drive_distance(50, 11)
          #  g.turn_with_gyro(-50, 50, 180)
            #u.move_servo(c.servoArm, c.armDown, 5)  # delivering firetruck
           # u.move_servo(c.servoClaw, c.clawOpen, 3)
          #  u.move_servo(c.servoArm, c.armUp, 3)
    else:   #right building on fire
        if c.isClone:
            g.turn_with_gyro(20, -20, 10)  # correcting turn to pick up firetruck
            d.drive_to_white_and_square_up(70)
            msleep(250)
            g.drive_distance(-50, 6)
            msleep(250)
            #d.drive_to_white_and_square_up(-70)
            d.drive_to_black_and_square_up(-70)
            msleep(250)
            g.turn_with_gyro(50, -50, 90)
            d.drive_till_black_right(-70)
            g.drive_distance(-70, 3)  # was 4
            u.move_servo(c.servoArm, c.armDown, 5)  # delivering firetruck
            msleep(100)
            u.move_servo(c.servoClaw, c.clawOpen, 6)
            msleep(100)
            msleep(100)
            u.move_servo(c.servoArm, c.armUp, 6)

        else:
            g.turn_with_gyro(-50, 50, 180)
            g.drive_distance(50, 1)
            u.waitForButton()
            g.turn_with_gyro(-50, 50, 2)
            u.waitForButton()
            g.drive_distance(50, 2)
            u.waitForButton()
            u.move_servo(c.servoArm, c.armDown, 5)  # delivering firetruck
            u.move_servo(c.servoClaw, c.clawOpen, 3)
            u.move_servo(c.servoArm, c.armUp, 3)
            u.waitForButton()
            g.drive_distance(-50, 2)
            g.turn_with_gyro(50, -50, 2)


def driveToValve():
    print("driving to valve")
    global leftBurning
    if leftBurning:
        pass
    else:
        d.drive_to_black_and_square_up(50)
        d.drive_to_white_and_square_up(70)
        msleep(250)
        g.pivot_on_right_wheel(70, 90)
        msleep(250)
        g.drive_distance(-70, 10)
        u.waitForButton()
        u.move_servo(c.servoArm, c.armValveGrab, 5)
        g.drive_distance(30, 3.75) #was 4
        msleep(250)
        u.waitForButton()
        u.move_servo(c.servoClaw, c.clawValve, 5)
        u.move_servo(c.servoArm, c.armValveGrab + 200, 2)
        u.waitForButton()
        g.drive_distance(30, 0.5)
        u.move_servo(c.servoArm, c.armUp, 2)
