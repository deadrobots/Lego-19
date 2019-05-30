import wallaby as w

# Time
start_time = -1

# Digital ports
CLONE_SWITCH = 9
RIGHT_BUTTON = 13
BUTTON = 0

#Prime/Clone
is_clone = w.digital(CLONE_SWITCH)
is_prime = not is_clone

# motor values
LEFT_MOTOR = 0
if is_prime:
    RIGHT_MOTOR = 3
else:
    RIGHT_MOTOR = 2

#Analog ports
FRONT_TOPHAT_RIGHT = 0  # analog
FRONT_TOPHAT_LEFT = 1
START_LIGHT = 5

#sensor values
on_black = 1800

#servo ports
servo_arm = 0
servo_wrist = 1
servo_claw = 3     #switched from 2 due to broken port

if is_clone: # Yellow Lego
    #arm
    arm_up = 1420
    arm_down = 180  # start position
    arm_valve_grab = 350
    arm_drop_off = 550
    armValve = 1000
    armValveDrop = 660
    armBinGrab = 163
    armBinPickup = 945

    #wrist
    wrist_horizontal = 80    # pipe held vertically
    wrist_vertical = 1250  # pipe held horizontally
    wristFlipped = 2040

    #claw
    claw_open = 0
    claw_closed = 700
    claw_bin = 860
    claw_valve = 850

    #gyro
    turn_conversion = 5260

if is_prime: # Red Lego
    # arm
    # Arm values are based on the tightness of the two screws in the arm
    # Make sure these are tight before you start to change arm values
    arm_up = 1420
    arm_down = 210 #230 old, missed pom often start position
    arm_valve_grab = 355 #370
    arm_drop_off = 550
    armValve = 1100
    armValveDrop = 695
    armBinGrab = 267
    armBinPickup = 945


    # wrist
    wrist_horizontal = 60 # wrist flat
    wrist_vertical = 1200 # wrist with upper and lower sides of claw
    wristFlipped = 2040

    # claw
    claw_open = 0  #150
    claw_closed = 1000
    claw_bin = 1170 # Estimated
    claw_bin_closed = 1024  #not yet used?????
    claw_valve = 1100

    # gyro
    turn_conversion = 5180 #5150
