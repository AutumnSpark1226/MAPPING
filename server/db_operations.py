"""
easy access to the database
see database_info.ods for information
"""

import os
from datetime import date
from secrets import compare_digest
from time import sleep

import analysis_algorithms
from driving_algorithm import sensor_max_distance
from lib import database

# table names
raw_data_table_name: str
objects_table_name: str
object_groups_table_name: str
divide_conquer_table_name: str
noisy_regions_table_name: str
# table locks
raw_data_table_locked = False
_objects_table_locked = False
_object_groups_table_locked = False
_divide_conquer_table_locked = False
_raw_data_table_entry_counter = 0


def connect(address="localhost", username="MAPPING_server", password="$$getFromFile$$",
            database_name='MAPPING', txt='DBPassword.txt') -> None:
    # do NOT use $$getFromFile as your password (please, I don't know what else to put here)
    if compare_digest(password, "$$getFromFile$$"):
        password = open(os.getcwd() + '/server/' + txt, 'r').readline().rstrip()
    database.connect(address, username, password, database_name)


def disconnect() -> None:
    database.disconnect()


def setup_database() -> None:
    if not database.does_table_exist('GENERAL'):
        # create table GENERAL
        database.execute(
            'CREATE TABLE GENERAL (ID int NOT NULL AUTO_INCREMENT, NAME varchar(100) NOT NULL, VALUE varchar(255), '
            'CHANGED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (ID))')
        # insert creation timestamp
        database.execute("INSERT INTO GENERAL (NAME, VALUE) VALUES ('created', '-> CHANGED')")
        # insert run_count
        database.execute("INSERT INTO GENERAL (NAME, VALUE) VALUES ('run_count', '0')")
        # insert raw_data_table_count
        database.execute("INSERT INTO GENERAL (NAME, VALUE) VALUES ('raw_data_table_count', '0')")
    create_raw_data_table()
    global objects_table_name, object_groups_table_name, divide_conquer_table_name, noisy_regions_table_name
    suffix = date.today().strftime("%Y%m%d") + '_' + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][0])
    objects_table_name = 'OBJECTS_' + suffix
    object_groups_table_name = 'OBJECT_GROUPS_' + suffix
    divide_conquer_table_name = 'DIVIDE_CONQUER_' + suffix
    noisy_regions_table_name = 'NOISY_REGIONS_' + suffix
    if not database.does_table_exist(objects_table_name):
        database.execute('CREATE TABLE ' + objects_table_name + ' (ID int NOT NULL AUTO_INCREMENT, POS_X int NOT NULL,'
                                                                ' POS_Y int NOT NULL, OBJECT_TYPE varchar(64), TIME '
                                                                'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                                                                'PRIMARY KEY (ID))')  # OBJECT_TYPE: varchar ===> enum
    if not database.does_table_exist(object_groups_table_name):
        # TODO WIP
        database.execute(
            'CREATE TABLE ' + object_groups_table_name + ' (ID int NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID))')
    if not database.does_table_exist(divide_conquer_table_name):
        database.execute(
            'CREATE TABLE ' + divide_conquer_table_name + '(ID int NOT NULL AUTO_INCREMENT, SQUARE_P0_X int NOT NULL, '
                                                          'SQUARE_P0_Y int NOT NULL, SQUARE_P1_X int NOT NULL, '
                                                          'SQUARE_P1_Y int NOT NULL, REAL_VALUE_PERCENTAGE double(6, '
                                                          '5), TIME timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                                                          'PRIMARY KEY (ID))')
    if not database.does_table_exist(noisy_regions_table_name):
        database.execute(
            'CREATE TABLE ' + noisy_regions_table_name + ' (ID int NOT NULL AUTO_INCREMENT, POS_X int NOT NULL,'
                                                         ' POS_Y int NOT NULL, OBJECT_TYPE varchar(64), TIME '
                                                         'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                                                         'PRIMARY KEY (ID))')
    # update run_count
    database.execute("UPDATE GENERAL SET VALUE = '" + str(
        int(database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][
                0]) + 1) + "' WHERE NAME='run_count'")


def clean() -> None:  # clean data from previous runs
    tables = database.fetch("SHOW TABLES")
    for table in tables:
        if table[0].startswith('RAW_DATA_') or table[0].startswith('OBJECTS_') or table[0].startswith('OBJECT_GROUPS_'):
            database.execute("DROP TABLE " + table[0])
    if database.does_table_exist('GENERAL'):
        database.execute("UPDATE GENERAL SET VALUE = '0' WHERE NAME='run_count' OR NAME='raw_data_table_count'")


def lock_raw_data_table() -> None:  # lock read operations
    global raw_data_table_locked
    raw_data_table_locked = True


def unlock_raw_data_table() -> None:  # unlock read operations
    global raw_data_table_locked
    raw_data_table_locked = False


def lock_objects_table() -> None:  # lock read operations
    global _objects_table_locked
    _objects_table_locked = True


def unlock_objects_table() -> None:  # unlock read operations
    global _objects_table_locked
    _objects_table_locked = False


def lock_object_groups_table() -> None:  # lock read operations
    global _object_groups_table_locked
    _object_groups_table_locked = True


def unlock_object_groups_table() -> None:  # unlock read operations
    global _object_groups_table_locked
    _object_groups_table_locked = False


def create_raw_data_table() -> None:
    # update raw_data_table_name
    global raw_data_table_name
    raw_data_table_name = 'RAW_DATA_' + date.today().strftime("%Y%m%d") + '_' + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][0]) + "_" + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='raw_data_table_count'")[0][0])
    # update raw_data_table_count in GENERAL
    database.execute("UPDATE GENERAL SET VALUE = '" + str(
        int(database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='raw_data_table_count'")[0][
                0]) + 1) + "' WHERE NAME='raw_data_table_count'")
    analysis_algorithms.thread0.current_id = 1
    if database.does_table_exist(raw_data_table_name):
        database.execute("DROP TABLE " + raw_data_table_name)  # delete the table if it exists for whatever reason
    # create raw data table
    database.execute(
        'CREATE TABLE ' + raw_data_table_name + ' (ID int NOT NULL AUTO_INCREMENT, POS_X int NOT NULL,'
                                                ' POS_Y int NOT NULL, DEGREES int NOT NULL, DISTANCE_S1 int, '
                                                'DISTANCE_S2 int, SENSOR_TYPE enum("S1.US,S2.US", "S1.IR,S2.IR", '
                                                '"S1.US,S2.IR", "S1.IR,S2.US", "S1.US", "S1.IR", "S2.US", '
                                                '"S2.IR", "S3.US") NOT NULL, TIME timestamp NOT'
                                                ' NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (ID))')


def write_raw_data(pos_x: int, pos_y: int, degrees: int, sensor_type: str, distance_s1=-1, distance_s2=-1) -> None:
    if distance_s1 == distance_s2 == -1:
        raise Exception("no value given")
    database.execute(
        "INSERT INTO " + raw_data_table_name + "(POS_X, POS_Y, DEGREES, DISTANCE_S1, DISTANCE_S2, SENSOR_TYPE) VALUES ("
        + str(pos_x) + ", " + str(pos_y) + ", " + str(degrees) + ", " + str(distance_s1) + ", " + str(
            distance_s2) + ", '" + sensor_type + "')")
    # TODO might result in errors; testing required
    # create a new table to save resources after 10000 (or maybe more) entries have been written
    global _raw_data_table_entry_counter
    _raw_data_table_entry_counter += 1
    if _raw_data_table_entry_counter >= 10000:
        _raw_data_table_entry_counter = 0
        analysis_algorithms.complete_primary_analysis()


def get_raw_data(entry_id: int) -> [int, int, int, int, int, str]:
    while raw_data_table_locked:
        sleep(0.5)
    sql_statement = "SELECT POS_X, POS_Y, DEGREES, DISTANCE_S1, DISTANCE_S2, SENSOR_TYPE FROM " + raw_data_table_name \
                    + " WHERE ID=" + str(entry_id)
    return database.fetch(sql_statement)[0]


def count_raw_data_entries() -> int:
    while raw_data_table_locked:
        sleep(0.5)
    return int(database.fetch("SELECT COUNT(ID) FROM " + raw_data_table_name)[0][0])


def write_object(pos_x: int, pos_y: int, object_type="undefined") -> None:
    database.execute("INSERT INTO " + objects_table_name + " (POS_X, POS_Y, OBJECT_TYPE) VALUES (" + str(pos_x) +
                     ", " + str(pos_y) + ", '" + object_type + "')")


def get_object(entry_id: int) -> [int, int, str]:
    while _objects_table_locked:
        sleep(0.5)
    sql_statement = "SELECT POS_X, POS_Y, OBJECT_TYPE FROM " + objects_table_name + " WHERE ID=" + str(entry_id)
    return database.fetch(sql_statement)[0]


def count_object_entries() -> int:
    while _objects_table_locked:
        sleep(0.5)
    return int(database.fetch("SELECT COUNT(ID) FROM " + objects_table_name)[0][0])


def write_scan_area(pos_x: int, pos_y: int, real_value_percentage: float) -> None:
    real_value_percentage = round(real_value_percentage, 5)
    square_p0_x = pos_x - ((2 * sensor_max_distance) ** 2) / 4
    square_p0_y = pos_y - ((2 * sensor_max_distance) ** 2) / 4
    square_p1_x = pos_x + ((2 * sensor_max_distance) ** 2) / 4
    square_p1_y = pos_y + ((2 * sensor_max_distance) ** 2) / 4
    database.execute(
        "INSERT INTO " + divide_conquer_table_name + "(SQUARE_P0_X, SQUARE_P0_Y, SQUARE_P1_X, SQUARE_P1_Y, "
                                                     "REAL_VALUE_PERCENTAGE) VALUES(" + square_p0_x + ", " +
        square_p0_y + ", " + square_p1_x + ", " + square_p1_y + ", " + str(
            real_value_percentage) + ")")


def write_line(p1, p2, degrees) -> None:
    print("WIP")
    # TODO WIP


def get_line(entry_id: int) -> [[int, int], [int, int], int]:
    print("WIP")
    # TODO WIP
    # return [p0_x, p0_y], [p1_x, p1_y], degrees
    return [0, 0], [0, 0], 0


def get_line_degrees(entry_id: int) -> int:
    print("WIP")
    # TODO WIP
    return 0


def write_noisy_region(pos_x: int, pos_y: int, object_type: str) -> None:
    database.execute("INSERT INTO " + noisy_regions_table_name + "(POS_X, POS_Y, OBJECT_TYPE) VALUES (" +
                     str(pos_x) + ", " + str(pos_y) + ", '" + object_type + "')")


def get_noisy_region() -> [int, int, str]:
    return database.fetch("SELECT POS_X, POS_Y, OBJECT_TYPE FORM " + noisy_regions_table_name + " LIMIT 1")[0]


def clear_noisy_regions() -> None:
    database.execute("DELETE FROM " + noisy_regions_table_name)
