#!/usr/bin/python
from wallaby import *
import wallaby as w  #pick one convention eventually
import utils as u
import constants as c
import gyroDrive as g
import drive as d


def driveTimed(left, right, time):
    motor(c.LEFT_MOTOR, left)
    motor(c.RIGHT_MOTOR, right)
    msleep(time)
    ao()

def sleep(time):
    driveTimed(0, 0, time)

def drive(left, right):
    motor(c.LEFT_MOTOR,left)
    motor(c.RIGHT_MOTOR,right)

def line_follow_left(time):
    sec = seconds()
    while(seconds()-sec<time):
        if(u.onBlackFront()):
            drive(40,70)#was 45
        else:
            drive(70,40)#was 45
    drive(0,0)

def line_follow_right(time):
    sec = seconds()
    while(seconds()-sec<time):
        if(u.onBlackFront()):
            drive(60,55)
        else:
            drive(55,60)
    drive(0,0)


def tick_drive(time, speed1, speed2):
    if speed1 > 1400:
        print("speed too fast. please pick a number under 1401.")
        speed1 = 1400
    if speed1 > 1400:  # You are checking for "edge-cases" here. This is solid coding. Well done! - LMB
        print("speed too fast. please pick a number under 1401.")
        speed2 = 1400
    mav(c.motorLeft, speed1)
    mav(c.motorRight, speed2)
    msleep(time)


def drive_till_black():
    while analog(c.tophat) < 3000:
        mav(1000)
        mav(1000)

# Loop break timers #

time = 0  # This represents how long to wait before breaking a loop.


def set_wait(DELAY):  # Sets wait time in seconds before breaking a loop.
    global time
    time = seconds() + DELAY


def get_wait():  # Used to break a loop after using "setWait". An example would be: setWiat(10) | while true and getWait(): do something().
    return seconds() < time


def on_black_front():
    return w.analog(c.FRONT_TOPHAT_RIGHT) > c.on_black


def timed_line_follow_left(time):
    sec = seconds() + time
    while seconds() < sec:
        if on_black_front():
            driveTimed(20, 90, 20)
        else:
            driveTimed(90, 20, 20)
        msleep(10)


def timed_line_follow_right(time):
    sec = seconds() + time
    while seconds() < sec:
        if analog(c.FRONT_TOPHAT_RIGHT) < 200:
            motor(c.LEFT_MOTOR, 30)
            motor(c.RIGHT_MOTOR, 100)
        elif analog(c.FRONT_TOPHAT_RIGHT) < 800:
            motor(c.LEFT_MOTOR, 60)
            motor(c.RIGHT_MOTOR, 80)
        elif analog(c.FRONT_TOPHAT_RIGHT) < 1400:
            motor(c.LEFT_MOTOR, 80)
            motor(c.RIGHT_MOTOR, 80)
        elif analog(c.FRONT_TOPHAT_RIGHT) < 2000:
            motor(c.LEFT_MOTOR, 80)
            motor(c.RIGHT_MOTOR, 60)
        else:
            motor(c.LEFT_MOTOR, 100)
            motor(c.RIGHT_MOTOR,30)
    g._freeze_motors()



def timed_line_follow_right_smooth(time):
    sec = seconds() + time
    while seconds() < sec:
        if not on_black_front():
            driveTimed(20, 40, 20)
        else:
            driveTimed(40, 20, 20)
        msleep(10)


def line_follow_right_smooth_count(amount):
    count = 0
    while count < amount:
        if not on_black_front():
            driveTimed(10, 30, 10)
            count = count + 1
        else:
            driveTimed(30, 10, 10)
            count = 0


def timed_line_follow_left_smooth(time):
    sec = seconds() + time
    while seconds() < sec:
        if on_black_left():
            driveTimed(20, 40, 20)
        else:
            driveTimed(40, 20, 20)
        msleep(10)

def timed_line_follow_left_right_side_line(time):
    sec = seconds() + time
    while seconds() < sec:
        if on_black_left():
            driveTimed(40,20,20)
        else:
            driveTimed(20,40,20)

def timedLineFollowRightSmooth(time):
    sec = seconds() + time
    while seconds() < sec:
        if on_black_right():
            driveTimed(40, 20, 20)
        else:
            driveTimed(20, 40, 20)
        msleep(10)


def timed_line_follow_left_black(time):  # follows on starboard side
    sec = seconds() + time
    while seconds() < sec:
        if onBlackBack():
            driveTimed(-90, -20, 20)
        else:
            driveTimed(-20, -90, 20)
        msleep(10)


def cross_black_front():
    while not on_black_front():  # wait for black
        pass
    while on_black_front():  # wait for white
        pass
    ao()


def on_black_right():
    return analog(c.FRONT_TOPHAT_RIGHT) > c.on_black


def on_black_left():
    return analog(c.FRONT_TOPHAT_LEFT) > c.on_black


def square_up_black(left_wheel_speed, right_wheel_speed): #Drives till black then squares up
    while left_wheel_speed != 0 or right_wheel_speed != 0:
        if on_black_left():
            left_wheel_speed = 0
        if on_black_right():
            right_wheel_speed = 0
        drive(left_wheel_speed, right_wheel_speed)
#
# def square_up_white(left_wheel_speed, right_wheel_speed): #Drives till white then squares up
#     drive(left_wheel_speed, right_wheel_speed)
#     while left_wheel_speed != 0 or right_wheel_speed != 0:
#         drive(left_wheel_speed, right_wheel_speed)
#         if not on_black_left():
#             left_wheel_speed = 0
#             drive(left_wheel_speed, right_wheel_speed)
#         if not on_black_right():
#             right_wheel_speed = 0
#             drive(left_wheel_speed, right_wheel_speed)
#     g._freeze_motors()


def drive_to_black_and_square_up(speed):
    #msleep(500)
    g.drive_condition(speed, on_white_left_and_right, True)    # Drives while neither tophat sees black
    print('SAW BLACK!!!', on_black_left(), on_black_right())
    d.square_up_black(speed/2, speed/2)
    msleep(250)


def on_white_left_and_right():
    return not on_black_left() and not on_black_right()


def drive_to_white_and_square_up(speed):
    #msleep(500)
    g.drive_condition(50, d.on_black_right and d.on_black_left, True)
    g.drive_distance(50, 0.5)
    d.square_up_black(-50, -50)
    g.drive_distance(50, 0.25)
    msleep(250)


def drive_till_black_right(speed):
    msleep(500)
    g.drive_condition(speed, d.on_black_right, False)
    msleep(250)