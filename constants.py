import wallaby as w

# Time
start_time = -1

# motor values
LEFT_MOTOR = 0
RIGHT_MOTOR = 3


# Digital ports
CLONE_SWITCH = 9
RIGHT_BUTTON = 13
BUTTON = 0

is_clone = w.digital(CLONE_SWITCH)
is_prime = not is_clone

#Analog ports
FRONT_TOPHAT_RIGHT = 0  # analog
FRONT_TOPHAT_LEFT = 1

#sensor values
on_black = 1800
on_silver = 1800

#servo ports
servo_arm = 0
servo_wrist = 1
servo_claw = 2

if is_clone: # Yellow Lego
    #arm
    arm_up = 1420
    arm_down = 160  # start position
    arm_valve_grab = 350
    arm_drop_off = 550
    armValve = 1100
    armValveDrop = 660

    #wrist
    wrist_horizontal = 0    # pipe held vertically
    wrist_vertical = 1030  # pipe held horizontally
    wristFlipped = 2040

    #claw
    claw_open = 0
    claw_closed = 700
    claw_valve = 850

    #gyro
    turn_conversion = 5200

if is_prime: # Red Lego
    # arm
    arm_up = 1420
    arm_down = 160 # start position
    arm_valve_grab = 330
    arm_drop_off = 550
    armValve = 1100
    armValveDrop = 660

    # wrist
    wrist_horizontal = 60 # wrist flat
    wrist_vertical = 1150 # wrist with upper and lower sides of claw
    wristFlipped = 2040

    # claw
    claw_open = 150
    claw_closed = 1000
    claw_valve = 1100

    # gyro
    turn_conversion = 5200