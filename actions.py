#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g

left_burning = 1


def init():
    #Prime Setup:
    #The square up surface on the back of the bot should be flush to the back of the SB
    #The left edge of the square up surface should be just to the left of the coupler
    #Just use the marks on the table :)
    if c.is_clone:
        print("Hi! I'm Clone.")
    else:
        print("Hi! I'm Prime.")
    enable_servos()
    msleep(500)
    print("Don't touch me, I'm calibrating!!!")
    g.calibrate_gyro()
    msleep(500)
    u.move_servo(c.servo_arm, c.arm_drop_off, 10)
    # test the motors
    d.driveTimed(50, 50, 1000)
    d.driveTimed(50, 0, 1000)
    d.driveTimed(-50, 0, 1000)
    print("testing wrist")
    u.move_servo(c.servo_wrist, c.wrist_vertical)
    if c.is_prime:
        msleep(300)
        u.move_servo(c.servo_wrist, c.wristFlipped)
        msleep(300)
    u.move_servo(c.servo_wrist, c.wrist_horizontal)
    print("testing claw")
    u.move_servo(c.servo_claw, c.claw_closed)
    u.move_servo(c.servo_claw, c.claw_open)
    print("testing tophat")
    g.drive_condition(50, d.on_black_left, False)
    g.drive_condition(50, d.on_silver_right, True)
    d.drive_to_white_and_square_up(50)
    print("testing arm")
    u.move_servo(c.servo_arm, c.arm_up, 10)
    u.move_servo(c.servo_arm, c.arm_down, 5)
    print("place in start posistion")
    u.waitForButton()
    g.calibrate_gyro()

def grab_cluster():
    global left_burning
    print("Waiting for something to press button")
    done = seconds() + 4.0
    while seconds() < done:  #waiting for Create to send MC order (which building is on fire)
        if digital(c.BUTTON) == 1:
            left_burning = 0
        msleep(10)
    if left_burning == 1:
        print("The burning medical center is on the LEFT")
    else:
         print("The burning medical center is on the RIGHT")
    print ("Grabbing cluster")
    g.drive_timed(50, 0.55)
    u.move_servo(c.servo_claw, c.claw_closed, 12)
    u.move_servo(c.servo_arm, c.arm_up, 15)
    g.drive_distance(80, 2)

def drive_to_MC():
    #Drives towards both medical centers
    print ("Driving to medical center")
    g.pivot_on_left_wheel(90, 90)
    g.drive_distance(95, 19)
    d.drive_to_black_and_square_up(90)  # squaring up on line next to water block
    g.drive_distance(-90, 3.5)
    g.pivot_on_right_wheel(90, 90)  # turn to face silver line

def drop_off_cluster():
    global left_burning
    print("Dropping off cluster")
    g.drive_distance(90, 14)  # driving towards silver line (tophats land just past silver line, on black)
    d.drive_to_white_and_square_up(90)  # square up on white (past black and silver line)
    if left_burning == 1:
        print("left burning")
        g.drive_distance(85, 2.3)
        g.turn_with_gyro(-70, 70, 90)  # turns and squares up on black
        g.drive_distance(80, 4)
    else:
        print("right burning")
        g.turn_with_gyro(0, 90, 60)         #wiggles to black line
        g.drive_distance(95, 3)
        g.turn_with_gyro(90, 0, 60)
        if c.is_prime:
            d.timed_line_follow_right_smooth(4.4) #line follows until there is almost no space between it and the pipe
        else:
            d.timed_line_follow_right_smooth(4.8)
        g.turn_with_gyro(-80, 80, 90)           #turns and squares up on black
    g.drive_condition(-70, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-70, -70)
    msleep(50)
    g.drive_distance(70, 1)
    u.move_servo(c.servo_arm, c.arm_drop_off, 8)   #drops off cluster
    u.move_servo(c.servo_claw, c.claw_open, 8)
    u.move_servo(c.servo_arm, c.arm_drop_off + 200, 5)
    u.move_servo(c.servo_arm, c.arm_up, 20)
    print ("Delivered!")
    g.drive_distance(80, 1)


def drive_to_firetruck():
    global left_burning
    print("Driving to firetruck")
    d.drive_to_black_and_square_up(-90)   #squares up on black
    if left_burning == 1:
        print("left burning routine")
        g.drive_distance(90, 3.5)
        g.pivot_on_left_wheel(90, 90)
    else:
        print("right burning routine")
        g.drive_distance(90, 5.5)
        g.pivot_on_left_wheel(90, 90)
        d.drive_to_black_and_square_up(95)
        d.drive_to_white_and_square_up(95)
        g.drive_distance(95, 4)
        d.drive_to_black_and_square_up(95)  # True #drives until the black line at the end of the medical center


def pick_up_firetruck():
    global left_burning
    print("Picking up firetruck")
    d.drive_to_white_and_square_up(90)
    if left_burning:
        print("left burning")
        pass
    else:
        print("right burning")
        if c.is_prime :
            g.turn_with_gyro(-80, 80, 5)
        else:
            g.turn_with_gyro(-80, 80, 4)
    g.drive_distance(-80, 2.5)
    u.move_servo(c.servo_arm, c.arm_down, 15)
    g.drive_distance(80, 2.5)
    u.move_servo(c.servo_claw, c.claw_closed, 10)
    u.move_servo(c.servo_arm, c.arm_up, 12)        #picks up firetruck


def drop_off_firetruck():
    print("drop off firetruck")
    global left_burning
    if left_burning == 1:
        print("left burning")
        d.drive_to_white_and_square_up(80)
        g.drive_distance(70, 0.5)
        g.turn_with_gyro(60, -60, 90)
        d.drive_till_black_right(-70)
        g.drive_distance(-80, 3)  # was 4
        u.move_servo(c.servo_arm, c.arm_down, 10)  # delivering firetruck
        u.move_servo(c.servo_claw, c.claw_open, 6)
        u.move_servo(c.servo_arm, c.arm_up, 12)
    else:   # right building on fire
        print("right burning")
        g.turn_with_gyro(-60, 60, 170)
        g.drive_distance(80, 1)
        g.turn_with_gyro(-80, 80, 2)
        g.drive_distance(90, 2)
        u.move_servo(c.servo_arm, c.arm_down, 15)  # delivering firetruck
        g.turn_with_gyro(-80, 80, 10)   # rotates closer to building
        u.move_servo(c.servo_claw, c.claw_open, 12)
        u.move_servo(c.servo_arm, c.arm_up, 20)
        g.turn_with_gyro(80, -80, 10)   # rotates back


def drive_to_valve():
    print("driving to valve")
    global left_burning
    if left_burning:
        print("left burning")
        g.drive_distance(80, 6.5)       #drives forward a bit after dropping off firetruck
        g.turn_with_gyro(70, -70, 90)       #turns to face valve
        u.move_servo(c.servo_arm, c.arm_valve_grab, 15)
        g.drive_distance(80, 9)                             #blind drives to cover more distance quickly
        u.move_servo(c.servo_wrist, c.wrist_horizontal, 15)
        if c.is_prime:
            d.timed_line_follow_left_smooth(1.7) #4.5
        else:
            d.timed_line_follow_left_smooth(2)      #line follows to get in perfect position
        msleep(100)
    else:                   #right burning
        print ("right burning")
        g.turn_with_gyro(80, -80, 34)
        g.drive_distance(80, 7.2)
        g.turn_with_gyro(-80, 80, 34)           #wiggles closer to the line
        u.move_servo(c.servo_arm, c.arm_valve_grab, 20)
        if c.is_prime:
            d.timed_line_follow_left_smooth(0.8)    #1.1
        else:
            d.timed_line_follow_left_smooth(1)            #line follows to get in perfect position
        g.turn_with_gyro(-80, 80, 5)            #turns in a little to grab the valve easier
        g.drive_distance(80, .4)


def pick_up_valve():
    print("picking up valve")
    u.move_servo(c.servo_claw, c.claw_valve, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off, 20)
    g.drive_distance(70, 0.5)
    u.move_servo(c.servo_arm, c.armValve, 20)
    u.move_servo(c.servo_wrist, c.wristFlipped, 20)         #grabs valve, raises arm, and flips it to have a mechanical
    g.drive_distance(-90, 1)                                #stop
    g.turn_with_gyro(80, -80, 90)
    g.drive_distance(-80, 2)
    d.drive_to_black_and_square_up(-80)
    msleep(100)
    g.drive_distance(95, 67)                   #skrt skrts across the board
    msleep(100)

def drop_first_valve():
    #Places the first valve in its final place
    print("dropping off first valve")
    g.turn_with_gyro(-70, 70, 90)
    d.drive_to_black_and_square_up(-70)         #squares up backward on the long black line across the board
    g.drive_distance(-95, 26)                   #squares up against the wall
    g.drive_distance(85, 5)
    g.turn_with_gyro(70, -70, 90)
    d.drive_to_black_and_square_up(70)
    d.drive_to_white_and_square_up(70)          #squares up on the little line perpendicular to the wall
    msleep(100)
    g.drive_distance(-50, 3.1)
    msleep(100)
    g.turn_with_gyro(50, -50, 90)           #turns to face valve
    msleep(100)
    if c.is_prime:
        g.drive_distance(-50, 4)
    else:
        g.drive_distance(-50, 3.8)      #3.5
    msleep(100)
    g.turn_with_gyro(30, -30, 25)           #turns slightly to make sure there is enough space to drop the arm
    u.move_servo(c.servo_arm, c.armValveDrop, 20)
    u.move_servo(c.servo_wrist, c.wrist_vertical, 20)
    g.turn_with_gyro(-30, 30, 20)
    g.drive_distance(50, .25) #.5
    g.turn_with_gyro(-30, 30, 10)
    u.move_servo(c.servo_claw, c.claw_open, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off - 100, 20)         #slides the valve onto the pipe
    print("Delivered!")
    g.drive_distance(-90, 7)

def grab_second_valve():
    print("grabbing second valve")
    msleep(100)
    g.turn_with_gyro(75, -75, 190)              #turns all the way around
    u.move_servo(c.servo_wrist, c.wrist_horizontal, 30)
    u.move_servo(c.servo_arm, c.arm_valve_grab, 20)
    g.drive_distance(90, 9)
    d.drive_to_black_and_square_up(-80)
    g.drive_distance(90, 7)
    g.turn_with_gyro(70, -70, 15)
    g.drive_distance(85, 4.3)
    g.turn_with_gyro(-60, 60, 5)
    u.move_servo(c.servo_claw, c.claw_valve, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off, 20)
    g.drive_distance(70, 0.5)
    u.move_servo(c.servo_arm, c.armValve, 20)
    u.move_servo(c.servo_wrist, c.wristFlipped, 20)         #grabs the second valve and flips it
    g.turn_with_gyro(60, -60, 5)
    d.drive_to_black_and_square_up(-80)         #squares up on the big middle line

def drop_second_valve():
    print("dropping off second valve")
    g.drive_distance(-95, 25)           #follows the same sequence as the first valve drop off
    g.drive_distance(85, 5)
    g.turn_with_gyro(80, -80, 90)
    d.drive_to_black_and_square_up(80)
    d.drive_to_white_and_square_up(80)
    g.drive_distance(-50, 3.1)
    msleep(100)
    g.turn_with_gyro(50, -50, 90)
    msleep(100)
    if c.is_prime:
        g.drive_distance(-50, 4)
    else:
        g.drive_distance(-50, 3.8)      #3.5
    msleep(100)
    g.turn_with_gyro(30, -30, 25)
    u.move_servo(c.servo_arm, c.armValveDrop, 20)
    u.move_servo(c.servo_wrist, c.wrist_vertical, 20)
    g.turn_with_gyro(-30, 30, 12)
    g.drive_distance(50, .25) #.5
    g.turn_with_gyro(-30, 30, 10)           #drops it off on the same side as the first one, holds valve in scoring position; end of routine
    print("holding the second valve on the pipe")

