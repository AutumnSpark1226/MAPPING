import math

import db_operations
import main


def crit_distance(robot_pos_x, robot_pos_y, object_pos, crit_value:int):
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
                # find direction of object
