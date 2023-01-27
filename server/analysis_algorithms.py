import math
import threading
from time import sleep
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

import db_operations


class AnalysisThread0(threading.Thread):  # primary analysis: position objects in coordinate system
    keep_alive = True
    dead = True
    current_id = 1

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread0'
        print('[server/analysis_algorithms.py] ' + self.thread_name + ' initialized')

    def run(self):
        self.dead = False
        while self.keep_alive:
            if db_operations.count_raw_data_entries() >= self.current_id:
                raw_data = db_operations.get_raw_data(self.current_id)
                primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], raw_data[5])
                primary_analysis(raw_data[0], raw_data[1], raw_data[2] + 180, raw_data[4], raw_data[5])
                self.current_id += 1
            else:
                sleep(1)
        self.dead = True


class AnalysisThread1(threading.Thread):  # primary analysis: find groups of objects
    keep_alive = True
    dead = True
    current_id = 1

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread1'
        print('[server/analysis_algorithms.py] ' + self.thread_name + ' initialized')

    def run(self):
        self.dead = False
        while self.keep_alive:
            # TODO WIP
            self.keep_alive = False
        self.dead = True


thread0 = AnalysisThread0()
thread1 = AnalysisThread1()


def complete_primary_analysis():
    thread0.keep_alive = False
    while not thread0.dead:
        sleep(0.5)
    while db_operations.count_raw_data_entries() >= thread0.current_id:
        raw_data = db_operations.get_raw_data(thread0.current_id)
        # "S1.US;S2.IR", "S1.IR;S2.US", "S1.US", "S1.IR", "S2.US", "S2.IR", "S3.US"
        if raw_data[5].__contains__("S1"):
            sensor_type = raw_data[5][raw_data[5].find("S1.") + 3:raw_data[5].find("S1.") + 5]
            primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], sensor_type)
        if raw_data[5].__contains__("S2"):
            sensor_type = raw_data[5][raw_data[5].find("S2.") + 3:raw_data[5].find("S2.") + 5]
            primary_analysis(raw_data[0], raw_data[1], raw_data[2] + 180, raw_data[4], sensor_type)
        if raw_data[5].__contains__("S3"):
            sensor_type = raw_data[5]
            primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], sensor_type)
        thread0.current_id += 1


def primary_analysis(pos_x: int, pos_y: int, angle: int, distance: int, sensor_type: str):
    if distance == -1:
        raise Exception("distance is -1")
    # TODO do some magic: error correction!!!! (depending on sensor type)
    if distance != 2550 and sensor_type == "US":
        dy = distance * math.sin(math.radians(angle))
        x = int(math.sqrt((distance ** 2) - (dy ** 2)) + pos_x)
        y = int(dy + pos_y)
        db_operations.write_object(x, y)
    else:
        print("[server/analysis_algorithms.py] not implemented")  # WIP


def secondary_analysis():
    id = 0
    id_other = 1
    # loop until id maxed out
    # loop until id_other maxed out
    point1 = db_operations.get_object(id)
    point2 = db_operations.get_object(id_other)
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]
    distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
    id_other = id_other + 1
    # loop end
    if distance < 20:
        line = Line2D([point1[0], point2[0]], [point1[1], point2[1]])
    id = id + 1
    id_other = id + 1
    # loop end


def start():
    thread0.start()
    thread1.start()


def stop():
    thread0.keep_alive = False
    thread1.keep_alive = False
    # wait for the thread to finish
    while not thread0.dead and thread1.dead:
        sleep(0.5)
