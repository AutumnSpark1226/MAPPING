import math
import random

import db_operations
import main
from lib.logging import log

robot_position = [0, 0]
robot_rotation = 0
critical_distance = False
sensor_max_distance = 2500


def crit_distance(crit_value: int):
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
            log("distance < crit_value", "driving_algorithm.crit_distance()")
            global critical_distance
            critical_distance = True
    # TODO find direction of object, do something


def move_to(x, y):
    global robot_position
    dx = x - robot_position[0]
    dy = y - robot_position[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)
    degrees = math.atan(dy / dx) - robot_rotation
    main.rotate(int(degrees))
    main.drive_forward(int(distance))
    main.validate_position()
    robot_position = [x, y]


def drive_randomly():
    main.rotate(random.randint(0, 360))
    main.drive_forward(random.randint(0, 50))


def change_position(amount):  # FIXME no difference in argument between x and y ??
    robot_position[0] = robot_position[0] + amount * math.sin(robot_rotation)
    robot_position[1] = robot_position[1] + amount * math.cos(robot_rotation)


def change_rotation(degrees: int):
    global robot_rotation
    robot_rotation += degrees


def divide_and_conquer(size_x=0, size_y=0):
    global sensor_max_distance
    sensor_max_distance = 2550  # FIXME why overwrite the standard value??
    stage = 0
    if size_x and size_y == 0:  # FIXME you mean: "size_x == 0 and size_y == 0"??
        if not critical_distance:
            while not critical_distance:
                for i in range(2):
                    for j in range(stage + 1):
                        main.measure()
                        main.drive_forward((((2 * sensor_max_distance) ** 2) / 4) * 2)
                        main.measure()  # FIXME measure two times??
                main.rotate(90)
        else:
            main.measure()
            main.drive_forward(-10)  # FIXME only 1cm??
            main.rotate(robot_rotation - db_operations.get_line_degrees())  # FIXME
            change_rotation(robot_rotation - db_operations.get_line_degrees())  # FIXME
    else:
        log("WIP", "driving_algorithm.divide_and_conquer()")
        # TODO split room in small enough squares and do the same as before


def prioritise_locations():
    # TODO find the locations where the most noise was and drive there
    # fix the map lol
    move_to(0, 0)
