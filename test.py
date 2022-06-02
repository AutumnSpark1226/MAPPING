#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor  # not found by PyCharm; pip install pybricks
from pybricks.ev3devices import UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port


def test1():
    # Initialize the EV3 brick.
    ev3 = EV3Brick()
    # Initialize a motor at port A.
    test_motor = Motor(Port.A)
    # Play a sound.
    ev3.speaker.beep()
    test_motor.run_time(500, 2000)
    # Play another beep sound.
    ev3.speaker.beep(1000, 500)
    ev3.speaker.set_volume(1000)
    ev3.speaker.say("Jeremias: failure")
    # measure distance
    ultrasonic = UltrasonicSensor(Port.S1)
    print("distance: " + str(ultrasonic.distance()))


if __name__ == '__main__':
    test1()
