import math
import random

import db_operations
import main

robot_pos = [0, 0]
robot_rot = 0

def crit_distance(robot_pos_x, robot_pos_y, object_pos, crit_value: int):
    i = 0
    while id < db_operations.count_object_entries():
        robot_pos_x = main.robot_position_x
        robot_pos_y = main.robot_position_y
        object_pos = db_operations.get_object(i)
        x_diff = object_pos[0] - robot_pos_x
        y_diff = object_pos[1] - robot_pos_y
        distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
        i += 1
        if distance < crit_value:
            print("distance < crit_value")
    # TODO find direction of object do something

def move_to(x, y):
    dx = x - robot_pos[0]
    dy = y - robot_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    angle = math.atan(dy/dx)
    dangle = angle - robot_rot
    main.rotate(dangle)
    main.drive_forward(distance)
    robot_pos = [x, y]


def drive_randomly():
    main.rotate(random.randint(0, 360))
    main.drive_forward(random.randint(0, 50))


def change_position(amount):
    robot_pos[0] = robot_pos[0] + amount * math.sin(robot_rot)
    robot_pos[1] = robot_pos[1] + amount * math.cos(robot_rot)

def change_rotation(amount):
    robot_rot + amount