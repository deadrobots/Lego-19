#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import motorsPlusPlus as mpp


def main():
    #a.init()
    #u.waitForButton()
    #a.grabCluster()
    mpp.drive_speed(24, 80)
    msleep(100)
    mpp.drive_speed(-24, 80)




if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main();