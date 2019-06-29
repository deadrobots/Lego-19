#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g



def main():
    #global seeding
    #u.motor_calibration()
    a.init()
    c.start_time = seconds()
    if a.seeding:
        print("seeding")
    else:
        print ("head 2 head")
    a.grab_cluster()
    a.drive_to_MC()
    a.drop_off_cluster()
    a.drive_to_firetruck()
    a.pick_up_firetruck()
    a.drop_off_firetruck()
    a.drive_to_bin()
    a.grab_bin()
    a.drive_to_valve_seeding()
    a.pick_up_valve()
    a.driveToGasLine()
    a.drop_first_valve()
    a.grab_second_valve()
    a.drop_second_valve()
    u.DEBUGwithWait()


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main();