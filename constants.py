import wallaby as w

# Time
startTime = -1

#motor values
LEFT_MOTOR = 3
RIGHT_MOTOR = 0

LMOTOR = 3
RMOTOR = 0

# Digital ports
CLONE_SWITCH = 9
RIGHT_BUTTON = 13

isClone = w.digital(CLONE_SWITCH)


#sensor values
tophat = 0

#servo ports
servoArm = 0
servoWrist = 1
servoClaw = 2

#arm
armUp = 1500
armDown = 120  #start position
armGrab = 200

#wrist
wristPipeVertical = 800  #pipe held vertically
wristPipeHorizontal = 1900  #pipe held horizontally

#claw
clawOpen = 0
clawClosed = 600


#gyro
bias = 0
turn_conversion = 5500