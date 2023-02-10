import math
import random

import db_operations
import main

robot_pos = [0, 0]
robot_rot = 0
critical_distance = False
sensor_max_distance = 2550


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
            main.log("distance < crit_value", "driving_algorithm.crit_distance()")
            global critical_distance
            critical_distance = True
    # TODO find direction of object, do something


def move_to(x, y):
    global robot_pos
    dx = x - robot_pos[0]
    dy = y - robot_pos[1]
    distance = math.sqrt(dx ** 2 + dy ** 2)
    angle = math.atan(dy / dx)
    dangle = angle - robot_rot
    main.rotate(int(dangle))
    main.drive_forward(int(distance))
    robot_pos = [x, y]


def drive_randomly():
    main.rotate(random.randint(0, 360))
    main.drive_forward(random.randint(0, 50))


def change_position(amount):
    robot_pos[0] = robot_pos[0] + amount * math.sin(robot_rot)
    robot_pos[1] = robot_pos[1] + amount * math.cos(robot_rot)


def change_rotation(amount):
    global robot_rot
    robot_rot += amount


def divide_and_conquer(size_x=0, size_y=0):
    global sensor_max_distance
    sensor_max_distance = 2550
    i = 0
    i2 = 0
    stage = 0
    if size_x and size_y == 0:
        if not critical_distance:
            while not critical_distance:
                while i < 2:
                    while i2 < stage + 1:
                        main.measure_at_current_location()
                        main.drive_forward((((2 * sensor_max_distance) ** 2) / 4) * 2)
                        main.measure_at_current_location()
                        i2 += 1
                    i += 1
                main.rotate(90)
        else:
            main.measure_at_current_location()
            main.drive_forward(-10)
            main.rotate(robot_rot - db_operations.get_line_angle())
            change_rotation(robot_rot - db_operations.get_line_angle())
    else:
        main.log("WIP", "driving_algorithm.divide_and_conquer()")
        # TODO split room in small enough squares and do the same as before


def prioritise_locations():
    # TODO find the locations where the most noise was and drive there
    # fix the map lol
    move_to(0, 0)
