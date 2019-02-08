import wallaby as w

# Time
startTime = -1

#motor values
LEFT_MOTOR = 3
RIGHT_MOTOR = 0


# Digital ports
CLONE_SWITCH = 9
RIGHT_BUTTON = 13
BUTTON = 0

isClone = w.digital(CLONE_SWITCH)

#Analog ports
FRONT_TOPHAT_RIGHT = 0  #analog
FRONT_TOPHAT_LEFT = 1

#sensor values
on_black = 1800
on_silver = 1800

#servo ports
servoArm = 0
servoWrist = 1
servoClaw = 2

#arm
armUp = 1420
armDown = 70  #start position
armGrab = 120
armDropOff = 550

#wrist
wristPipeVertical = 800  #pipe held vertically
wristPipeHorizontal = 1900  #pipe held horizontally

#claw
clawOpen = 0
clawClosed = 700


#gyro
bias = 0
turn_conversion = 5200