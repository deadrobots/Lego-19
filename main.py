#!/usr/bin/python
import os, sys
from wallaby import *
import constants as c
import actions as a
import camera as m


def main():
    print("hello!")
    a.tickDrive(1000,1000,1000)



if __name__ == "__main__":
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)
main();