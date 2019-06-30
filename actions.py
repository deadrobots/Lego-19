#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g
import threading as t

left_burning = 1

seeding = True


def init():
    # Prime Setup:
    # The square up surface on the back of the bot should be flush to the back of the SB
    # The left edge of the square up surface should be just to the left of the coupler
    # Just use the marks on the table :)
    global seeding
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
    msleep(300)
    u.move_servo(c.servo_wrist, c.wristFlipped)
    msleep(300)
    u.move_servo(c.servo_wrist, c.wrist_horizontal)
    print("testing claw")
    u.move_servo(c.servo_claw, c.claw_closed)
    u.move_servo(c.servo_claw, c.claw_open)
    print("testing LEFT tophat")
    g.drive_condition(50, d.on_black_left, False)
    g.drive_distance(-50, 1)
    print("testing RIGHT tophat")
    g.drive_condition(50, d.on_black_right, False)
    g.drive_distance(-50, 1)
    g.drive_distance(50, 3)
    d.drive_to_white_and_square_up(50)
    print("Testing lever switch. Press it!")
    done = seconds() + 3.0
    while digital(c.BUTTON) != 1:
        if seconds() >= done:
            print("I'm waiting for you to press the switch...")
            done = seconds() + 4.0
        pass
    print("testing arm")
    u.move_servo(c.servo_arm, c.arm_up, 10)
    u.move_servo(c.servo_arm, c.arm_down-40, 5)
    seeding = True
    msleep(500)
    print("place in start posistion")
    ao()
    u.wait_4_light()
    #u.waitForButton()
    # shut_down_in(119.2)
    g.calibrate_gyro()


def grab_cluster():
    global left_burning
    print("Waiting for something to press button")
    u.move_servo(c.servo_arm, c.arm_down, 5)
    done = seconds() + 2.0
    while seconds() < done:  # waiting for Create to send MC order (which building is on fire)
        if digital(c.BUTTON) == 1:
            left_burning = 0
        msleep(10)
    if left_burning == 1:
        print("The burning medical center is on the LEFT")
    else:
         print("The burning medical center is on the RIGHT")
    print ("Grabbing cluster")
    g.drive_timed(50, 0.35) #was .55
    u.move_servo(c.servo_claw, c.claw_closed, 12)
    u.thread_servo(c.servo_arm, c.arm_valve_grab, 15)
    g.drive_distance(80, 2)


def drive_to_MC():
    #Drives towards both medical centers
    print ("Driving to medical center")
    if c.is_prime:
        g.pivot_on_left_wheel(90, 92)
    else:
        g.pivot_on_left_wheel(90, 92)
    # u.move_servo(c.servo_arm, c.arm_up)
    #u.thread_servo(c.servo_arm, c.arm_up, 10)
    u.move_servo(c.servo_arm, c.arm_up, 10)
    msleep(100)
    g.drive_distance(95, 19)
    d.drive_to_black_and_square_up(50)  # squaring up on line next to water block
    g.drive_distance(-90, 3.5)
    g.pivot_on_right_wheel(90, 90)  # turn to face silver line


def drop_off_cluster():
    global left_burning
    print("Dropping off cluster")
    g.drive_distance(90, 14)  # driving towards silver line
    d.drive_to_white_and_square_up(90)  # square up on white
    if left_burning == 1:
        print("left burning")
        if c.is_prime:
            g.drive_distance(85, 1.95)
        else:
            g.drive_distance(85, 2.15)
        g.turn_with_gyro(-70, 70, 90)
        g.drive_distance(80, 4.5)
    else:
        print("right burning")
        g.turn_with_gyro(0, 90, 75)  # wiggles to black line
        g.drive_distance(95, 3)
        g.turn_with_gyro(90, 0, 75)
        if c.is_prime:
            d.timed_line_follow_right_smooth(4.5)  # line follows until there is almost no space between it and the pipe
        else:
            d.timed_line_follow_right_smooth(4.8)
        g.turn_with_gyro(-70, 70, 90)  # turns and squares up on black
    g.drive_condition(-80, d.on_black_right or d.on_black_left, True)
    d.square_up_black(-75, -75)
    msleep(50)
    g.drive_distance(85, 1)
    if c.is_prime:
        u.move_servo(c.servo_arm, c.arm_drop_off, 12)  # drops off cluster
        u.move_servo(c.servo_claw, c.claw_open, 10)
        u.move_servo(c.servo_arm, c.arm_drop_off + 200, 10)
        u.move_servo(c.servo_arm, c.arm_up, 20)
    else:
        if left_burning == 1:
            g.turn_with_gyro(-25, 25, 2)  # with new claw design, this over rotates, so I'm commenting out
        u.move_servo(c.servo_arm, c.arm_drop_off, 12)  # drops off cluster
        u.move_servo(c.servo_claw, c.claw_open, 10)
        u.move_servo(c.servo_arm, c.arm_drop_off + 200, 10)
        u.move_servo(c.servo_arm, c.arm_up, 20)
        if left_burning == 1:
            g.turn_with_gyro(25, -25, 2)  # with new claw design, this over rotates, so I'm commenting out

    print ("Delivered!")
    g.drive_distance(80, 1)


def drive_to_firetruck():
    global left_burning
    print("Driving to firetruck")
    d.drive_to_black_and_square_up(-90)  # squares up on black
    if left_burning == 1:
        print("left burning routine")
        g.drive_distance(90, 3.5)
        g.pivot_on_left_wheel(90, 90)
    else:
        print("right burning routine")
        g.drive_distance(90, 4.9) #4.4
        if c.is_prime:
            g.pivot_on_left_wheel(90, 88)
            d.drive_to_white_and_square_up(95)
        else:
            g.pivot_on_left_wheel(90, 88)#90
            #d.drive_to_black_and_square_up(95)
            d.drive_to_white_and_square_up(95)
        g.drive_distance(95, 9)#
        d.drive_to_black_and_square_up(95)  # True #drives until the black line at the end of the medical center


def pick_up_firetruck():
    global left_burning
    print("Picking up firetruck")
    d.drive_to_white_and_square_up(90)
    if left_burning:
        print("left burning")
        if c.is_prime:
            g.turn_with_gyro(-70, 70, 2)
        else:
            pass
            #g.turn_with_gyro(-70, 70, 1)#4
    else:
        print("right burning")
        if c.is_prime:
            g.turn_with_gyro(-70, 70, 8)
        else:
            g.turn_with_gyro(-80, 80, 5)
    msleep(100)
    g.drive_distance(-90, 2.5)
    u.move_servo(c.servo_arm, c.arm_down, 20)
    g.drive_distance(90, 2.5)
    u.move_servo(c.servo_claw, c.claw_closed, 13)
    msleep(100)
    # u.thread_servo(c.servo_arm, c.arm_up, 17)
    u.move_servo(c.servo_arm, c.arm_up, 17)  # picks up firetruck


def drop_off_firetruck():
    print("drop off firetruck")
    global left_burning
    if left_burning == 1:
        print("left burning")
        d.drive_to_white_and_square_up(80)
        g.drive_distance(70, 0.5)
        g.turn_with_gyro(60, -60, 90)
        d.drive_till_black_right(-80)
        g.drive_distance(-80, 3)
        u.move_servo(c.servo_arm, c.arm_down, 15)  # delivering firetruck
        g.turn_with_gyro(70, -70, 10)
        u.move_servo(c.servo_claw, c.claw_open, 10)
        u.move_servo(c.servo_arm, c.arm_up, 14)
        g.turn_with_gyro(-70, 70, 10)
    else:  # right building on fire
        print("right burning")
        g.turn_with_gyro(-70, 70, 170)
        g.drive_distance(85, 1)
        g.turn_with_gyro(-80, 80, 2)
        g.drive_distance(90, 2)
        u.move_servo(c.servo_arm, c.arm_down, 15)  # delivering firetruck
        g.turn_with_gyro(-80, 80, 10)  # rotates closer to building
        u.move_servo(c.servo_claw, c.claw_open, 15)
        g.turn_with_gyro(70, -70, 5)
        u.move_servo(c.servo_arm, c.arm_up, 15)
        g.turn_with_gyro(80, -80, 10)  # rotates back


def drive_to_bin():
    print("driving to bin")
    global left_burning
    if left_burning:
        print("left burning")
        g.drive_distance(85, 6.5)
        g.turn_with_gyro(85, -85, 120)  # turns to face valve
        g.drive_distance(80, 3)
        g.turn_with_gyro(-85, 85, 20)
        set_servo_position(c.servo_wrist, c.wrist_vertical)
        d.timed_line_follow_left_right_side_line(3.5)
        g.drive_distance(85, 3.2)
        u.move_servo(c.servo_arm, c.arm_valve_grab, 30)   #maybe omit if you need to cut more time
        d.timed_line_follow_left_right_side_line(2.1)#2
        u.move_servo(c.servo_arm, c.armBinGrab, 25)
        msleep(50)
    else:  # right burning
        print ("right burning")
        g.turn_with_gyro(85, -85, 34)
        g.drive_distance(85, 7.1)
        g.drive_distance(85, 2)
        g.turn_with_gyro(0, 80, 34)  # wiggles closer to the line
        set_servo_position(c.servo_wrist, c.wrist_vertical)
        d.timed_line_follow_left_right_side_line(2)  # line follows to get in perfect position
        u.move_servo(c.servo_arm, c.armBinGrab, 25)
        d.timed_line_follow_left_right_side_line(.9)


def grab_bin():
    msleep(50)
    u.move_servo(c.servo_claw, c.claw_bin, 30)
    msleep(100)
    if left_burning:
        u.move_servo(c.servo_arm, c.arm_up, 22)
    else:
        u.move_servo(c.servo_arm, c.arm_up, 15) #22
    g.drive_distance(-100, 13.5)
    g.turn_with_gyro(-70, 70, 110)
    u.move_servo(c.servo_arm, c.arm_down + 60, 15)
    u.move_servo(c.servo_claw, c.claw_open, 15)
    msleep(50)
    u.move_servo(c.servo_arm, c.arm_up, 15)
    g.turn_with_gyro(70, -70, 20)
    g.drive_distance(90, 3)
    g.turn_with_gyro(70, -70, 90)
    #g.turn_with_gyro(-70, 70, 160)



def drive_to_valve_seeding():
    print("driving to valve")
    #g.pivot_on_right_wheel(-70, 90) #-70, 90
    msleep(100)
    u.move_servo(c.servo_arm, c.arm_up, 30)
    set_servo_position(c.servo_wrist, c.wrist_horizontal)
    if c.is_prime:
        u.move_servo(c.servo_arm, c.arm_valve_grab, 30)
    else:
        u.move_servo(c.servo_arm, c.arm_valve_grab - 5, 30)
    d.timed_line_follow_left_smooth(1) #1.25  # do not edit distance bc.line follow is not messed up (due to perpendicular black line)
    if c.is_prime:
        g.drive_distance(80, 2.6)
        d.timed_line_follow_left_smooth(1)  #1.15 # 1.45 was a bit too far
    else:
        g.drive_distance(80, 2.6)
        d.timed_line_follow_left_smooth(1.40)


def pick_up_valve():
    print("picking up valve")
    g.turn_with_gyro(-70, 70, 3)
    g.drive_distance(80, .3)
    u.move_servo(c.servo_claw, c.claw_valve, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off, 20)
    g.drive_distance(70, 0.5)
    u.move_servo(c.servo_arm, c.armValve, 20)
    u.move_servo(c.servo_wrist, c.wristFlipped, 20)  # grabs valve, raises arm, and flips it for a mechanical stop
    g.turn_with_gyro(-60, 60, 35)
    g.drive_distance(-70, 7)
    g.turn_with_gyro(60, -60, 35)
    d.drive_to_black_and_square_up(-70)

    if c.is_prime:
        g.drive_distance(-70, 1.7)#.7
    else:
        g.drive_distance(-70, 2)#1.5


def driveToGasLine():
    u.move_servo(c.servo_arm, 1400, 15)
    msleep(100)
    if c.is_prime:
        g.pivot_on_left_wheel(-85, 97)
        if left_burning:
            msleep(3400)  # pause for choreography
        else:
            msleep(100)
        g.drive_distance(100, 55.5)#95
    else:
        g.pivot_on_left_wheel(-85, 93)
        if left_burning:
            msleep(4900)
        else:
            msleep(1100)
        g.drive_distance(95, 58)


def drop_first_valve():
    # Places the first valve in its final place
    print("dropping off first valve")
    if c.is_prime:
        g.turn_with_gyro(-70, 70, 92)
        g.drive_distance(-100, 23)  # squares up against the wall
    else:
        g.turn_with_gyro(-70, 70, 90)
        g.drive_distance(-95, 23)  # squares up against the wall
    print('manual square up completed')
    g.drive_distance(85, 5)
    msleep(100)
    g.turn_with_gyro(70, -70, 90)
    msleep(100)
    d.drive_to_black_and_square_up(80)
    g.drive_distance(85, .5)
    d.drive_to_white_and_square_up(80)  # squares up on the little line perpendicular to the wall
    msleep(100)
    g.drive_distance(-60, 3.1)
    if c.is_prime:
        g.turn_with_gyro(50, -50, 92)  # turns to face valve
        msleep(100)
        g.drive_distance(-50, 4.6)
        msleep(100)
        g.turn_with_gyro(30, -30, 25)  # turns slightly to make sure there is enough space to drop the arm
    else:
        g.turn_with_gyro(50, -50, 90)
        msleep(100)
        g.drive_distance(-50, 5.1)  # 4.4
        msleep(100)
        g.turn_with_gyro(30, -30, 15)  # 10 # turns slightly to make sure there is enough space to drop the arm
    u.move_servo(c.servo_arm, c.armValveDrop, 20)
    u.move_servo(c.servo_wrist, c.wrist_vertical, 20)
    g.turn_with_gyro(-30, 30, 20)
    if c.is_prime:
        g.drive_distance(50, .4)
        g.turn_with_gyro(-30, 30, 20)#15
    else:
        g.drive_distance(50, .25)
        g.turn_with_gyro(-30, 30, 10)
    u.move_servo(c.servo_claw, c.claw_open, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off , 20)  # slides the valve onto the pipe
    print("Delivered with a spin!")
    # if c.is_prime:
    #     msleep(6000)  # pauses to keep from crashing into create
    # else:
    #     msleep(6000)
    g.drive_distance(-90, 7)


def grab_second_valve():
    print("grabbing second valve")
    msleep(100)
    if c.is_prime:
        g.turn_with_gyro(75, -75, 190)
    else:
        g.turn_with_gyro(75, -75, 195)  #190
    set_servo_position(c.servo_wrist, c.wrist_horizontal)  # turns wrist horizontally
    u.thread_servo(c.servo_arm, c.arm_up, 25)
    #g.drive_condition(90, d.on_black_right, False)##########
    g.drive_distance(90, 8)
    #g.drive_distance(90, 3)################
    d.drive_to_black_and_square_up(-80)
    if c.is_prime:
        g.drive_distance(90, 5)  # lego drove towards orange valve before turning
        g.turn_with_gyro(70, -70, 23)
        u.move_servo(c.servo_arm, c.arm_valve_grab, 20)
        g.drive_distance(85, 6.0)  # 5.0
        g.turn_with_gyro(-60, 60, 8)
        g.drive_distance(60, .6)#.4
    else:
        g.drive_distance(90, 5)  # lego drove towards orange valve before turning
        g.turn_with_gyro(70, -70, 22)  # 17 gave problem twice
        u.move_servo(c.servo_arm, c.arm_valve_grab, 20)
        g.drive_distance(85, 6.1)  #5.9 came up short
        g.turn_with_gyro(-60, 60, 8)
        g.drive_distance(60, .2)
    u.move_servo(c.servo_claw, c.claw_valve, 20)
    u.move_servo(c.servo_arm, c.arm_drop_off, 20)
    if c.is_prime:
        g.drive_distance(70, .5)    #0.7
    else:
        g.drive_distance(70, .7)
    u.move_servo(c.servo_arm, c.armValve, 20)
    u.move_servo(c.servo_wrist, c.wristFlipped, 20)  # grabs the second valve and flips it
    g.turn_with_gyro(60, -60, 5)
    g.drive_distance(-70, 5)
    d.drive_to_black_and_square_up(-75)  # squares up on the big middle line


def drop_second_valve():
    print("dropping off second valve")
    if c.is_prime:
        g.drive_distance(-100, 25)  # follows the same sequence as the first valve drop off
    else:
        g.drive_distance(-95, 25)
    g.drive_distance(85, 5)
    g.turn_with_gyro(80, -80, 90)
    d.drive_to_black_and_square_up(80)
    g.drive_distance(85, .5)
    d.drive_to_white_and_square_up(80)
    u.move_servo(c.servo_arm, c.arm_up, 15)
    g.drive_distance(-70, 3.1)
    msleep(100)
    g.turn_with_gyro(70, -70, 90)
    msleep(100)
    if c.is_prime:
        g.drive_distance(-50, 4.4)
    else:
        g.drive_distance(-80, 4.4)  # 4.2
    msleep(100)
    g.turn_with_gyro(50, -50, 25)
    u.move_servo(c.servo_arm, c.armValveDrop, 20)
    u.move_servo(c.servo_wrist, c.wrist_vertical, 20)
    g.turn_with_gyro(-50, 50, 20)
    g.drive_distance(75, .25)
    g.turn_with_gyro(-50, 50, 10)  # drops off on the same side as the first valve, holds valve in scoring position
    # end of lego routine
    print("holding the second valve on the pipe")


def flip_bin_over():
    print("preparing to grab bin")
    u.waitForButton()  #for now, place bin after arm sets up for grab
    print("picking up bin")
    u.move_servo(c.servo_arm, c.armBinPickup, 20)
    msleep(200)
    u.move_servo(c.servo_claw, c.claw_bin, 20)
    msleep(200)
    u.move_servo(c.servo_arm, c.armBinPickup, 10)
    g.drive_distance(-40, 14)

