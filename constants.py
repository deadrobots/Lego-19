import wallaby as w

# Time
startTime = -1

# motor values
LEFT_MOTOR = 0
RIGHT_MOTOR = 3


# Digital ports
CLONE_SWITCH = 9
RIGHT_BUTTON = 13
BUTTON = 0

isClone = w.digital(CLONE_SWITCH)
isPrime = not isClone

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

if isClone: # Yellow Lego
    #arm
    armUp = 1420
    armDown = 70  # start position
    armGrab = 120
    armValveGrab = 350
    armDropOff = 600

    #wrist
    wristHorizontal = 425  #pipe held vertically
    wristVertical = 1525  #pipe held horizontally

    #claw
    clawOpen = 0
    clawClosed = 700
    clawValve = 850

    #gyro
    bias = 0
    turn_conversion = 5200

if isPrime: # Red Lego
    # arm
    armUp = 1420
    armDown = 150 #300 # start position #was 100
   # armGrab = 120
    armDropOff = 550

    # wrist
    wristHorizontal = 425 # wrist flat
    wristVertical = 1525 # wrist with upper and lower sides of claw

    # claw
    clawOpen = 100
    clawClosed = 900
    clawValve = 950

    # gyro
    turn_conversion = 5200