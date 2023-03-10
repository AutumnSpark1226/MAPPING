#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port

motor_a = Motor(Port.A)
motor_d = Motor(Port.D)

ev3 = EV3Brick()


def demo():
    motor_a.run_angle(450, 360)  # rotate tower
    motor_d.run_time(200, 5000)  # drive forward


if __name__ == "__main__":
    demo()
