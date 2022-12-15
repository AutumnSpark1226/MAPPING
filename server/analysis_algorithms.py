import threading
from time import sleep

import db_operations


class AnalysisThread0(threading.Thread):  # primary analysis: position objects in coordinate system
    keep_alive = True
    current_id = 1

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread0'
        print('[server/analysis_algorithms.py] ' + self.thread_name + ' initialized')

    def run(self):
        while self.keep_alive:
            if db_operations.count_raw_data_entries() > self.current_id:
                raw_data = db_operations.get_raw_data(self.current_id)
                primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], raw_data[4])
                self.current_id += 1
            else:
                sleep(1)


thread0 = AnalysisThread0()


def complete_primary_analysis():
    thread0.keep_alive = False
    while db_operations.count_raw_data_entries() > thread0.current_id:
        raw_data = db_operations.get_raw_data(thread0.current_id)
        primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], raw_data[4])
        thread0.current_id += 1


def primary_analysis(pos_x: int, pos_y: int, angle: int, distance_s1: int, distance_s2: int):
    print("WIP")


def start():
    thread0.start()


def stop():
    thread0.keep_alive = False
