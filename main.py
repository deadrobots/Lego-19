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
    a.driveToMC()
    u.waitForButton()
    a.dropOffCluster()
    a.driveToFiretruck()
    a.pickUpFiretruck()
    a.dropOffFiretruck()

if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
    main();