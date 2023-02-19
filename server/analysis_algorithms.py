import math
import threading
from time import sleep

import database
import db_operations
from main import log


class AnalysisThread0(threading.Thread):  # primary analysis: position objects in coordinate system
    keep_alive = True
    dead = True
    current_id = 1
    analysis_finished = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread0'
        log('initialized', self.thread_name)

    def run(self):
        self.dead = False
        while self.keep_alive or not self.analysis_finished:
            if self.current_id <= db_operations.count_raw_data_entries():
                self.analysis_finished = False
                thread1.analysis_finished = False
                db_operations.lock_objects_table()
                raw_data = db_operations.get_raw_data(self.current_id)
                # "S1.US,S2.US", "S1.IR,S2.IR, "S1.US,S2.IR", "S1.IR,S2.US", "S1.US", "S1.IR", "S2.US", "S2.IR", "S3.US"
                if raw_data[5].__contains__("S1"):
                    sensor_type = raw_data[5][raw_data[5].find("S1.") + 3:raw_data[5].find("S1.") + 5]
                    primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], sensor_type)
                if raw_data[5].__contains__("S2"):
                    sensor_type = raw_data[5][raw_data[5].find("S2.") + 3:raw_data[5].find("S2.") + 5]
                    primary_analysis(raw_data[0], raw_data[1], raw_data[2] + 180, raw_data[4], sensor_type)
                if raw_data[5].__contains__("S3"):
                    sensor_type = raw_data[5]
                    primary_analysis(raw_data[0], raw_data[1], raw_data[2], raw_data[3], sensor_type)
                self.current_id += 1
            else:
                db_operations.unlock_objects_table()
                self.analysis_finished = True
                sleep(1)
        self.dead = True

    def stop(self):
        self.keep_alive = False
        while not self.dead:
            sleep(0.5)


class AnalysisThread1(threading.Thread):  # secondary analysis: find groups of objects
    keep_alive = True
    dead = True
    analysis_finished = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'AnalysisThread1'
        log('initialized', self.thread_name)

    def run(self):
        self.dead = False
        id0 = 1
        id1 = 2
        while self.keep_alive or not self.analysis_finished:
            if id0 < db_operations.count_object_entries():
                self.analysis_finished = False
                while id1 < db_operations.count_object_entries():
                    point1 = db_operations.get_object(id0)
                    point2 = db_operations.get_object(id1)
                    x_diff = point2[0] - point1[0]
                    y_diff = point2[1] - point1[1]
                    distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
                    id1 += 1
                    if distance < 20:  # TODO real world tests (might require fine tuning)
                        log("P1: " + str(point1), self.thread_name)
                        log("P2: " + str(point2), self.thread_name)
                        # TODO calculate degrees
                        # TODO write to db
                id0 += 1
                id1 = id0 + 1
            else:
                self.analysis_finished = True
                sleep(0.5)
        self.dead = True

    def stop(self):
        self.keep_alive = False
        while not self.dead:
            sleep(0.5)


thread0 = AnalysisThread0()
thread1 = AnalysisThread1()


def primary_analysis(pos_x: int, pos_y: int, degrees: int, distance: int, sensor_type: str):
    if distance == -1:
        log("distance is -1", "analysis_algorithms.primary_analysis()")
        raise Exception("distance is -1")
    # TODO do some magic: error correction!!!! (depending on sensor type)
    if distance != 2550 and sensor_type == "US":
        dy = distance * math.sin(math.radians(degrees))
        x = int(math.sqrt((distance ** 2) - (dy ** 2)) + pos_x)
        y = int(dy + pos_y)
        db_operations.write_object(x, y)
    else:
        log("not implemented", "analysis_algorithms.primary_analysis()")  # WIP


def detect_noise():  # TODO testing required
    while not thread0.analysis_finished:
        sleep(0.5)
    entries_count = database.fetch("SELECT COUNT(ID) FROM " + db_operations.objects_table_name)[0][0]
    # Compute the mean of the x-coordinates and y-coordinates
    x_mean = database.fetch("SELECT SUM(POS_X) FROM " + db_operations.objects_table_name)[0][0] / entries_count
    y_mean = database.fetch("SELECT SUM(POS_Y) FROM " + db_operations.objects_table_name)[0][0] / entries_count
    # Compute the standard deviation of the x-coordinates and y-coordinates
    standard_deviation_x = int((database.fetch(
        "SELECT SUM(POWER((POS_X - " + x_mean + "), 2)) FROM " + db_operations.objects_table_name)[0][
                                    0] / entries_count) ** 0.5)
    standard_deviation_y = int((database.fetch(
        "SELECT SUM(POWER((POS_Y - " + y_mean + "), 2)) FROM " + db_operations.objects_table_name)[0][
                                    0] / entries_count) ** 0.5)
    # Find the coordinates that are more than 3 standard deviations away from the mean
    outliers = database.fetch(
        "SELECT POS_X, POS_Y, OBJECT_TYPE FROM " + db_operations.objects_table_name + " WHERE ABS(POS_X - " + x_mean +
        ") > " + str(
            3 * standard_deviation_x) + " OR ABS(POS_Y - " + y_mean + ") > " + str(3 * standard_deviation_y))
    return outliers  # TODO write to DB??


def start():
    thread0.start()
    thread1.start()


def complete_primary_analysis():
    global thread0
    db_operations.unlock_raw_data_table()
    thread0.stop()
    db_operations.lock_raw_data_table()
    db_operations.create_raw_data_table()
    thread0 = AnalysisThread0()
    thread0.start()


def stop():
    thread0.stop()
    thread1.stop()
