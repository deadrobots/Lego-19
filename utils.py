#!/usr/bin/python
from wallaby import *
import constants as c
import gyroDrive as g


def driveTimed(left, right, time):
    motor(c.LEFT_MOTOR, left)
    motor(c.RIGHT_MOTOR, right)
    msleep(time)
    ao()

def waitForButton():
    print("Press Right Button...")
    while not digital(c.RIGHT_BUTTON):
        pass
    msleep(1)
    print("Pressed")
    msleep(1000)

def DEBUG():
    freeze(c.LEFT_MOTOR)
    freeze(c.RIGHT_MOTOR)
    print('Program stop for DEBUG\nSeconds: ', seconds() - c.start_time)
    ao()
    exit(0)

def DEBUGwithWait():
    freeze(c.LEFT_MOTOR)
    freeze(c.RIGHT_MOTOR)
    print ('Program stop for DEBUG\nSeconds: ', seconds() - c.start_time)
    ao()
    msleep(5000)

def sleep(time):
    driveTimed(0, 0, time)

def drive(left, right):
    motor(c.LEFT_MOTOR, left)
    motor(c.RIGHT_MOTOR, right)

######################################
def wait_4_light(ignore=False):
    if ignore:
        waitForButton()
        return
    while not calibrate(c.START_LIGHT):
        pass
    _wait_4(c.START_LIGHT)


def calibrate(port):
    print("Press LEFT button with light on")
    while not left_button():
        pass
    while left_button():
        pass
    lightOn = analog(port)
    print("On value =", lightOn)
    if lightOn > 200:
        print("Bad calibration")
        return False
    msleep(1000)
    print("Press RIGHT button with light off")
    while not right_button():
        pass
    while right_button():
        pass
    lightOff = analog(port)
    print("Off value =", lightOff)
    if lightOff < 3000:
        print("Bad calibration")
        return False

    if (lightOff - lightOn) < 2000:
        print("Bad calibration")
        return False
    c.startLightThresh = (lightOff - lightOn) / 2
    print("Good calibration! ", c.startLightThresh)
    return True


def _wait_4(port):
    print("waiting for light!! ")
    while analog(port) > c.startLightThresh:
        pass
#####################################

def move_servo(servo, endPos, speed=10):
    now = get_servo_position(servo)
    if now > 2047:
        print("Servo setting too large ", servo)
    if now < 0:
        print("Servo setting too small ", servo)
    if now > endPos:
        speed = -speed
    for i in range(now, endPos, speed):
        set_servo_position(servo, i)
        msleep(10)
    set_servo_position(servo, endPos)
    msleep(10)

def motor_calibration():
    move_servo(c.servo_arm, c.arm_up)
    msleep(1000)
    g.calibrate_gyro()
    print("Distance calibration:")
    print("Place the robot square against some wall or edge, then")
    waitForButton()
    g.drive_distance(80, 30)
    g.drive_timed(0,0)
    print("Measure distance traveled.")
    print("If greater than 30 inches, decrease inches-to-ticks value in gyroDrive")
    print("If less than 30 inches, increase inches-to-ticks value")
    print("---")
    waitForButton()
    print("Turning calibration:")
    print("Orient the robot parallel to a tape line")
    waitForButton()
    g.turn_with_gyro(60, -60, 180)
    g.drive_timed(0,0)
    msleep(100)
    print("If robot overturns, decrease turn_conversion in constants.")
    print("If robot underturns, increase turn_conversion in constants.")
    DEBUG()

