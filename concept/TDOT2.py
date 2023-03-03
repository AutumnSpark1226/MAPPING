#!/usr/bin/env pybricks-micropython

from pybricks.ev3devices import Motor  # not found by PyCharm; working
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
engineA = Motor(Port.A)
engineD = Motor(Port.D)

ev3 = EV3Brick()

def demo():
    engineA.run_time(500, 2000)
    engineD.run_time(500, 2000)

if __name__ == "__main__":
    demo()
