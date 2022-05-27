#!/usr/bin/env python3

import math
import random

from pybricks.ev3devices import Motor  # not found by PyCharm; pip install pybricks
from pybricks.ev3devices import UltrasonicSensor
from pybricks.hubs import EV3Brick
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
ev3.speaker.say("Jeremias: failure")
# measure distance
ultrasonic = UltrasonicSensor(Port.S1)
print("distance: " + str(ultrasonic.distance()))
