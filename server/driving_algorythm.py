import math
import random

from pybricks.ev3devices import Motor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port

import db_operations
import main
import server

ev3 = EV3Brick()
engineA = Motor(Port.A)
climberB = Motor(Port.B)
rotatorC = Motor(Port.C)


def rotate(degrees: int):
    server.send_text("rotate" + degrees)


def drive(cm: int):
    server.send_text("drive_forward" + cm)


def crit_distance(robot_pos_x, robot_pos_y, object_pos, crit_value: int):
    id = 0
    while id < db_operations.count_object_entries():
        robot_pos_x = main.robot_position_x
        robot_pos_y = main.robot_position_y
        object_pos = db_operations.get_object(id)
        x_diff = object_pos[0] - robot_pos_x
        y_diff = object_pos[1] - robot_pos_y
        distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
        id += 1
        if distance < crit_value:
    # TODO find direction of object do something


def drive_randomly():
    rotate(random.randint(0, 360))
    drive(random.randint(0, 100))
