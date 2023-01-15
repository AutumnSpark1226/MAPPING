import math
import threading
from time import sleep

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


thread0 = AnalysisThread0()


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
        print("not implemented")  # WIP


def start():
    thread0.start()


def stop():
    thread0.keep_alive = False
    # wait for the thread to finish
    while not thread0.dead:
        sleep(0.5)
