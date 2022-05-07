#!/usr/bin/env pybricks-micropython
# TODO performance test with python3 and pybricks-micropython -> performance_test.sh

# example program

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor  # TODO not found by PyCharm; maybe: from ._common import Motor
from pybricks.ev3devices import UltrasonicSensor
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
print("distance" + str(ultrasonic.distance()))

