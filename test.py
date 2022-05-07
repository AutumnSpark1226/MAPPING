#!/usr/bin/env python3

# example program


import math
import random

from pybricks.ev3devices import Motor  # not found by PyCharm; seems to be working on the robot
from pybricks.ev3devices import UltrasonicSensor
from pybricks.hubs import EV3Brick  # pip install pybricks
from pybricks.parameters import Port

# Initialize the EV3 brick.
ev3 = EV3Brick()
# Initialize a motor at port A.
test_motor = Motor(Port.A)
# Play a sound.
ev3.speaker.beep()
# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
test_motor.run_target(500, 90)
# Play another beep sound.
ev3.speaker.beep(1000, 500)
# say hi
ev3.speaker.say("Hi, i'm a robot")
# measure distance
ultrasonic = UltrasonicSensor(Port.S1)
print("distance: " + str(ultrasonic.distance()))
# generate a random number
print(random.randint(-255, 255))
# do some calculations
print(math.sqrt(234234 * 4323535))
