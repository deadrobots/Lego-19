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
        print("The burning medical center is on the left")
    else:
         print("The burning medical center is on the right")
    print ("Grabbing cluster")
    g.drive_timed(60, 0.55)
    u.move_servo(c.servo_claw, c.claw_closed, 10)
    msleep(100)
    u.move_servo(c.servo_arm, c.arm_up, 10)
    msleep(100)
    g.drive_distance(70, 2)

def drive_to_MC():
    #Drives towards both medical centers
    print ("Driving to medical center")
    g.pivot_on_left_wheel(75, 90)
    d.drive_to_black_and_square_up(70)
    d.drive_to_white_and_square_up(70)
    g.drive_distance(95, 15)
    d.drive_to_black_and_square_up(70)  # squaring up on line next to water block
    g.drive_distance(-70, 3.5)
    g.pivot_on_right_wheel(70, 90)  # turn to face silver line

def drop_off_cluster():
    global left_burning
    print("Dropping off cluster")
    g.drive_distance(70, 14)  # driving towards silver line (tophats land just past silver line, on black)
    d.drive_to_white_and_square_up(70)  # square up on white (past black and silver line)
    if left_burning == 1:
        if c.is_clone:
            g.drive_distance(60, 2)
        else:
            g.drive_distance(60, 2.3)
        g.turn_with_gyro(-50, 50, 90)  # turns and squares up on black
        g.drive_distance(50, 4)
    else:
        g.turn_with_gyro(0, 70, 60)         #wiggles to black line
        g.drive_distance(70, 3)
        g.turn_with_gyro(70, 0, 60)
        d.timed_line_follow_right_smooth(4.4) #line follows until there is almost no space between it and the pipe
        g.turn_with_gyro(-70, 70, 90)           #turns and squares up on black
        msleep(100)
    g.drive_condition(-30, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-30, -30)
    msleep(100)
    if c.is_prime:
        g.drive_distance(50, 1)
    else:
        g.drive_distance(30, 0.5)
    u.move_servo(c.servo_arm, c.arm_drop_off, 5)   #drops off cluster
    u.move_servo(c.servo_claw, c.claw_open, 5)
    u.move_servo(c.servo_arm, c.arm_drop_off + 200, 3)
    u.move_servo(c.servo_arm, c.arm_up, 10)
    print ("Delivered!")
    msleep(100)
    if c.is_clone:
        if left_burning == 1:
            g.drive_distance(40, 1)
    else:
        g.drive_distance(50, 1)


def drive_to_firetruck():
    global left_burning
    print("Driving to firetruck")
    d.drive_to_black_and_square_up(-60)   #squares up on black
    if c.is_clone:
        g.drive_distance(50, 6.0)
    else:
        if left_burning == 1:
            g.drive_distance(50, 3.5)
        else:
            g.drive_distance(70, 5.5)
    #g.turn_with_gyro(-50, 50, 90)
    if left_burning == 1:
        g.pivot_on_left_wheel(50, 90)   #turns and drives forward to square up on black line
    else:
        g.pivot_on_left_wheel(70, 90)
    #g.drive_distance(-50, 4)
    if left_burning == 1:                #switched code from else to left
        print("left burning routine")
        #d.drive_to_black_and_square_up(70)
        pass
    else:
        print("right burning routine")
        d.drive_to_black_and_square_up(70)
        d.drive_to_white_and_square_up(70)
        g.drive_distance(70, 4)
        d.drive_to_black_and_square_up(70) #True #drives until the black line at the end of the medical center


def pick_up_firetruck():
    global left_burning
    print("Picking up firetruck")
    d.drive_to_white_and_square_up(70)
    if c.is_clone:
        g.turn_with_gyro(-25, 25, 10)
    else:
        if left_burning:
            pass
        else:
            g.turn_with_gyro(-30, 30, 5)
    if c.is_clone:
        g.drive_distance(-50, 0.75) #1
    else:
        g.drive_distance(-50, 2.5)
    u.move_servo(c.servo_arm, c.arm_down, 10)
    if c.is_clone:
        pass
    else:
        g.drive_distance(50, 2.5)
    u.move_servo(c.servo_claw, c.claw_closed, 10)
    msleep(100)
    u.move_servo(c.servo_arm, c.arm_up, 10)        #picks up firetruck
    msleep(100)


def drop_off_firetruck():
    print ("drop off firetruck")
    global left_burning
    if left_burning == 1:
        if c.is_clone:
            g.turn_with_gyro(20, -20, 10)           #correcting turn to pick up firetruck
            d.drive_to_white_and_square_up(70)
            msleep(250)
            g.turn_with_gyro(50, -50, 90)
            d.drive_till_black_right(-70)
            g.drive_distance(-70, 3) #was 4
            u.move_servo(c.servo_arm, c.arm_down, 5)  #delivering firetruck
            msleep(100)
            u.move_servo(c.servo_claw, c.claw_open, 6)
            msleep(100)
            msleep(100)
            u.move_servo(c.servo_arm, c.arm_up, 6)
        else:
            # This is a copy and paste of the current strategy for clone, but it doesn't work (at all)
            # Please work to make these firetruck pick up and drop offs more consistent for P + C
            d.drive_to_white_and_square_up(70)
            msleep(250)
            g.drive_distance(70, 0.5)
            msleep(100)
            g.turn_with_gyro(50, -50, 90)
            d.drive_till_black_right(-70)
            g.drive_distance(-70, 3)  # was 4
            u.move_servo(c.servo_arm, c.arm_down, 5)  # delivering firetruck
            msleep(100)
            u.move_servo(c.servo_claw, c.claw_open, 6)
            msleep(100)
            msleep(100)
            u.move_servo(c.servo_arm, c.arm_up, 6)
            # g.drive_distance(50, 11)
            # g.turn_with_gyro(-50, 50, 180)
            # u.move_servo(c.servoArm, c.armDown, 5)  # delivering firetruck
            # u.move_servo(c.servoClaw, c.clawOpen, 3)
            # u.move_servo(c.servoArm, c.armUp, 3)
    else:   # right building on fire
        if c.is_clone:
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
            u.move_servo(c.servo_arm, c.arm_down, 5)  # delivering firetruck
            msleep(100)
            u.move_servo(c.servo_claw, c.claw_open, 6)
            msleep(100)
            msleep(100)
            u.move_servo(c.servo_arm, c.arm_up, 6)
        else:
            g.turn_with_gyro(-60, 60, 174)
            g.drive_distance(60, 1)
            g.turn_with_gyro(-60, 60, 2)
            g.drive_distance(60, 2)
            u.move_servo(c.servo_arm, c.arm_down, 10)  # delivering firetruck
            g.turn_with_gyro(-60, 60, 10)   # rotates closer to building
            u.move_servo(c.servo_claw, c.claw_open, 10)
            u.move_servo(c.servo_arm, c.arm_up, 10)
            g.turn_with_gyro(60, -60, 10)   # rotates back


def drive_to_valve():
    print("driving to valve")
    global left_burning
    if left_burning:
        g.drive_distance(70, 6.5)
        msleep(100)
        g.turn_with_gyro(70, -70, 90)
        msleep(100)
        u.move_servo(c.servo_arm, c.arm_valve_grab, 10)
        msleep(100)
        g.drive_distance(70, 9)
        msleep(100)
        u.move_servo(c.servo_wrist, c.wrist_horizontal, 5)
        d.timed_line_follow_left_smooth(1.9) #4.5
        msleep(100)
    else:
        g.turn_with_gyro(70, -70, 34)
        g.drive_distance(70, 7.2)
        g.turn_with_gyro(-70, 70, 34)
        u.move_servo(c.servo_arm, c.arm_valve_grab, 20)
        d.timed_line_follow_left_smooth(1)
        g.turn_with_gyro(-60, 60, 5)


def pick_up_valve():
    print("picking up valve")
    u.move_servo(c.servo_claw, c.claw_valve, 10)
    u.move_servo(c.servo_arm, c.arm_drop_off, 10)
    g.drive_distance(50, 0.5)
    u.move_servo(c.servo_arm, c.armValve, 10)
    u.move_servo(c.servo_wrist, c.wristFlipped, 20)
    g.drive_distance(-70, 1)
    g.turn_with_gyro(70, -70, 90)
    g.drive_distance(-30, 2)
    d.drive_to_black_and_square_up(-70)
    msleep(100)
    g.drive_distance(95, 67)
    msleep(100)

def drop_first_valve():
    #Places the first valve in its final place
    g.turn_with_gyro(-70, 70, 90)
    d.drive_to_black_and_square_up(-70)
    g.drive_distance(-80, 25)
    g.drive_distance(80, 5)
    g.turn_with_gyro(70, -70, 90)
    d.drive_to_black_and_square_up(70)
    d.drive_to_white_and_square_up(70)
    msleep(100)
    g.drive_distance(-50, 3.1)
    msleep(100)
    g.turn_with_gyro(50, -50, 90)
    msleep(100)
    g.drive_distance(-50, 4)
    msleep(100)
    g.turn_with_gyro(30, -30, 25)
    u.move_servo(c.servo_arm, c.armValveDrop, 20)
    u.move_servo(c.servo_wrist, c.wrist_vertical, 20)
    g.turn_with_gyro(-30, 30, 20)
    g.drive_distance(50, .25) #.5
    g.turn_with_gyro(-30, 30, 10)
    u.move_servo(c.servo_claw, c.claw_open, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off - 100, 20)
    g.drive_distance(-90, 7)

def grab_second_valve():
    msleep(100)
    g.turn_with_gyro(80, -80, 190)
    u.move_servo(c.servo_wrist, c.wrist_horizontal, 30)
    u.move_servo(c.servo_arm, c.arm_valve_grab, 20)
    g.drive_distance(90, 9)
    d.drive_to_black_and_square_up(-80)
    g.drive_distance(90, 7)
    g.turn_with_gyro(60, -60, 15)
    g.drive_distance(60, 4.3)
    g.turn_with_gyro(-60, 60, 5)
    u.move_servo(c.servo_claw, c.claw_valve, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off, 20)
    g.drive_distance(70, 0.5)
    u.move_servo(c.servo_arm, c.armValve, 20)
    u.move_servo(c.servo_wrist, c.wristFlipped, 20)
    g.turn_with_gyro(60, -60, 5)
    d.drive_to_black_and_square_up(-80)

def drop_second_valve():
    g.drive_distance(-80, 25)
    g.drive_distance(80, 5)
    g.turn_with_gyro(80, -80, 90)
    d.drive_to_black_and_square_up(80)
    d.drive_to_white_and_square_up(80)
    g.drive_distance(-50, 3.1)
    msleep(100)
    g.turn_with_gyro(50, -50, 90)
    msleep(100)
    g.drive_distance(-50, 4)
    msleep(100)
    g.turn_with_gyro(30, -30, 25)
    u.move_servo(c.servo_arm, c.armValveDrop, 20)
    u.move_servo(c.servo_wrist, c.wrist_vertical, 20)
    g.turn_with_gyro(-30, 30, 12)
    g.drive_distance(50, .25) #.5
    g.turn_with_gyro(-30, 30, 10)
    #Success! Currently finishes run at 121 seconds scoring 420 points
    #Work on slight speed changes to cut down the 1 second
    #Make sure it works consistently
    #Start to brainstorm other things LEGO can do

