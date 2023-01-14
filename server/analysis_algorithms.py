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
                primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3])
                primary_analysis(raw_data[0], raw_data[1], raw_data[2] + 180, raw_data[4])
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
        primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3])
        primary_analysis(raw_data[0], raw_data[1], raw_data[2] + 180, raw_data[4])
        thread0.current_id += 1


def primary_analysis(pos_x: int, pos_y: int, angle: int, distance: int):
    if distance != 2550:
        dy = distance * int(math.sin(angle))
        x = int(math.sqrt((distance ** 2) - (dy ** 2)) + pos_x)
        y = dy + pos_y
        print(angle)
        print(distance)
        print(x)
        print(y)
        print()
        db_operations.write_object(x, y)


def start():
    thread0.start()


def stop():
    thread0.keep_alive = False
    # wait for the thread to finish
    while not thread0.dead:
        sleep(0.5)
