#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import utils as u
import drive as d
import gyroDrive as g


def main():
    a.init()
    u.waitForButton()
    a.grabCluster()
    u.waitForButton()
    a.driveToMC()


if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main();