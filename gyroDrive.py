#!/usr/bin/python
from wallaby import *
import math
import constants as c
import utils as u

if c.is_prime:
    INCHES_TO_TICKS = 222 #195
else:
    INCHES_TO_TICKS = 195


bias = 0


def _clear_ticks():
    clear_motor_position_counter(c.RIGHT_MOTOR)
    clear_motor_position_counter(c.LEFT_MOTOR)


def _freeze_motors():
    motor(c.LEFT_MOTOR, 0)
    motor(c.RIGHT_MOTOR, 0)


def calibrate_gyro():
    i = 0
    avg = 0
    while i < 100:
        avg = avg + gyro_z()
        msleep(1)
        i = i + 1
    global bias
    bias = avg/i
    msleep(60)

#The drive functions use the change in gyro_z to adjust wheel speeds and drive straight
def drive_timed(speed, time):
    #print("Driving for time")
    #calibrate_gyro()
    start_time = seconds()
    theta = 0
    while seconds() - start_time < time:
        if speed > 0:
            motor(c.RIGHT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956*theta))))
            motor(c.LEFT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956*theta))))
        else:
             motor(c.RIGHT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956*theta))))
             motor(c.LEFT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956*theta))))
        msleep(10)
        theta = theta + (gyro_z() - bias) * 10
    _freeze_motors()

                                                  # All of these turn/pivots measure the change gyro_z to make the turn or pivot more excact
def turn_with_gyro(left_wheel_speed, right_wheel_speed, target_theta_deg):
    #calibrate_gyro()
    #print("turning")
    target_theta = round(target_theta_deg * c.turn_conversion)
    theta = 0
    while theta < target_theta:
        motor(c.RIGHT_MOTOR, right_wheel_speed)
        motor(c.LEFT_MOTOR, left_wheel_speed)
        msleep(10)
        theta = theta + abs(gyro_z() - bias) * 10
    #print(theta)
    _freeze_motors()


def pivot_on_left_wheel(right_wheel_speed, target_theta_deg):
    #calibrate_gyro()
    #print("pivoting on left")
    target_theta = round(target_theta_deg * c.turn_conversion)
    theta = 0
    while theta < target_theta:
        motor(c.RIGHT_MOTOR, right_wheel_speed)
        motor(c.LEFT_MOTOR, 0)
        msleep(10)
        theta = theta + abs(gyro_z() - bias) * 10
    motor(c.LEFT_MOTOR, 0)
    motor(c.RIGHT_MOTOR, 0)
    _freeze_motors()


def pivot_on_right_wheel(left_wheel_speed, target_theta_deg):
    #calibrate_gyro()
    #print("pivoting on right")
    target_theta = round(target_theta_deg * c.turn_conversion)
    theta = 0
    while theta < target_theta:
        motor(c.RIGHT_MOTOR, 0)
        motor(c.LEFT_MOTOR, left_wheel_speed)
        msleep(10)
        theta = theta + abs(gyro_z() - bias) * 10
    motor(c.LEFT_MOTOR, 0)
    motor(c.RIGHT_MOTOR, 0)
    _freeze_motors()


def drive_distance(speed, distance):
    #calibrate_gyro()
    _clear_ticks()
    #print("Driving for distance")
    theta = 0
    while abs((get_motor_position_counter(c.RIGHT_MOTOR) + get_motor_position_counter(c.LEFT_MOTOR))/2) < distance * INCHES_TO_TICKS:
        if speed > 0:
            motor(c.RIGHT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956*theta))))
            motor(c.LEFT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956*theta))))
        else:
             motor(c.RIGHT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956*theta))))
             motor(c.LEFT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956*theta))))
        msleep(10)
        theta = theta + (gyro_z() - bias) * 10
    _freeze_motors()


def drive_condition(speed, test_function, state = True): #Needs some work
    #calibrate_gyro()
    #print("Driving while condition is inputted state")
    theta = 0
    while test_function() is state:
        if speed > 0:
            motor(c.RIGHT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956 * theta))))
            motor(c.LEFT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956 * theta))))
        else:
            motor(c.RIGHT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956 * theta))))
            motor(c.LEFT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956 * theta))))
        msleep(10)
        theta = theta + (gyro_z() - bias) * 10
    _freeze_motors()


def _drive(speed):
    #calibrate_gyro()
    theta = 0
    while True:
        if speed > 0:
            motor(c.RIGHT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956*theta))))
            motor(c.LEFT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956*theta))))
        else:
             motor(c.RIGHT_MOTOR, int((speed + speed * (1.920137e-16 + 0.000004470956*theta))))
             motor(c.LEFT_MOTOR, int((speed - speed * (1.920137e-16 + 0.000004470956*theta))))
        msleep(10)
        theta = theta + (gyro_z() - bias) * 10
    _freeze_motors()


def _drive1(lspeed, rspeed, theta = 0):
    #calibrate_gyro()
    if rspeed > 0:
        motor(c.RIGHT_MOTOR, int((rspeed - rspeed * (1.920137e-16 + 0.000004470956*theta))))
        motor(c.LEFT_MOTOR, int((lspeed + lspeed * (1.920137e-16 + 0.000004470956*theta))))
    else:
        motor(c.RIGHT_MOTOR, int((rspeed + rspeed * (1.920137e-16 + 0.000004470956*theta))))
        motor(c.LEFT_MOTOR, int((lspeed - lspeed * (1.920137e-16 + 0.000004470956*theta))))
    msleep(10)


def drive_timed1(lspeed, rspeed, time):
    #calibrate_gyro()
    #print("Driving for time")
    start_time = seconds()
    theta = 0
    while seconds() - start_time < time:
        if lspeed > 0:
            motor(c.RIGHT_MOTOR, int((rspeed - rspeed * (1.920137e-16 + 0.000004470956*theta))))
            motor(c.LEFT_MOTOR, int((lspeed + lspeed * (1.920137e-16 + 0.000004470956*theta))))
        else:
             motor(c.RIGHT_MOTOR, int((rspeed + rspeed * (1.920137e-16 + 0.000004470956*theta))))
             motor(c.LEFT_MOTOR, int((lspeed - lspeed * (1.920137e-16 + 0.000004470956*theta))))
        msleep(10)
        theta = theta + (gyro_z() - bias) * 10
    _freeze_motors()

