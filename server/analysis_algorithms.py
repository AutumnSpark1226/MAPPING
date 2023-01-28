import math
import threading
from time import sleep

from matplotlib.lines import Line2D

import db_operations


class AnalysisThread0(threading.Thread):  # primary analysis: position objects in coordinate system
    keep_alive = True
    dead = True
    current_id = 1
    analysis_finished = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread0'
        print('[server/analysis_algorithms.py] ' + self.thread_name + ' initialized')

    def run(self):
        self.dead = False
        while self.keep_alive:
            if self.current_id <= db_operations.count_raw_data_entries():
                self.analysis_finished = False
                thread1.lock()
                raw_data = db_operations.get_raw_data(self.current_id)
                # "S1.US;S2.IR", "S1.IR;S2.US", "S1.US", "S1.IR", "S2.US", "S2.IR", "S3.US"
                if raw_data[5].__contains__("S1"):
                    sensor_type = raw_data[5][raw_data[5].find("S1.") + 3:raw_data[5].find("S1.") + 5]
                    print(sensor_type)
                    primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], sensor_type)
                if raw_data[5].__contains__("S2"):
                    sensor_type = raw_data[5][raw_data[5].find("S2.") + 3:raw_data[5].find("S2.") + 5]
                    print(sensor_type)
                    primary_analysis(raw_data[0], raw_data[1], raw_data[2] + 180, raw_data[4], sensor_type)
                if raw_data[5].__contains__("S3"):
                    sensor_type = raw_data[5]
                    print(sensor_type)
                    primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], sensor_type)
                self.current_id += 1
            else:
                self.analysis_finished = True
                thread1.unlock()
                sleep(1)
        self.dead = True

    def stop(self):
        self.keep_alive = False
        while not self.dead:
            sleep(0.5)


class AnalysisThread1(threading.Thread):  # secondary analysis: find groups of objects
    keep_alive = True
    dead = True
    _locked = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread1'
        print('[server/analysis_algorithms.py] ' + self.thread_name + ' initialized')

    def run(self):
        self.dead = False
        id0 = 0
        id1 = 1
        while self.keep_alive:
            while self._locked:
                sleep(0.5)
            if id0 < db_operations.count_object_entries():
                while id1 < db_operations.count_object_entries():
                    point1 = db_operations.get_object(id0)
                    point2 = db_operations.get_object(id1)
                    x_diff = point2[0] - point1[0]
                    y_diff = point2[1] - point1[1]
                    distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
                    id1 += 1
                    if distance < 20:
                        line = Line2D([point1[0], point2[0]], [point1[1], point2[1]])
                id0 += 1
                id1 = id0 + 1
            else:
                sleep(1)
        self.dead = True

    def stop(self):
        self.keep_alive = False
        while not self.dead:
            sleep(0.5)

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False


thread0 = AnalysisThread0()
thread1 = AnalysisThread1()


def primary_analysis(pos_x: int, pos_y: int, angle: int, distance: int, sensor_type: str):
    if distance == -1:
        raise Exception("distance is -1")
    # TODO do some magic: error correction!!!! (depending on sensor type)
    if distance != 2550 and sensor_type == "US":
        dy = distance * math.sin(math.radians(angle))
        x = int(math.sqrt((distance ** 2) - (dy ** 2)) + pos_x)
        y = int(dy + pos_y)
        db_operations.write_object(x, y)
        print("DEBUG: object_written")
    # else:
    #    print("[server/analysis_algorithms.py] not implemented")  # WIP


def start():
    thread0.start()
    thread1.start()


def complete_primary_analysis():
    global thread0
    db_operations.unlock()
    thread0.stop()
    db_operations.lock()
    db_operations.create_raw_data_table()
    thread0 = AnalysisThread0()
    thread0.start()


def stop():
    thread0.stop()
    thread1.stop()
