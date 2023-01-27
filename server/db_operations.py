"""
easy access to the database
see database_info.ods for information
"""

import os
from datetime import date
from secrets import compare_digest

import analysis_algorithms
from lib import database

raw_data_table_name: str
objects_table_name: str
object_groups_table_name: str


def connect(address="localhost", username="MAPPING_server", password="$$getFromFile$$",
            database_name='MAPPING'):  #
    # do NOT use $$getFromFile as your password (please, I don't know what else to put here)
    if compare_digest(password, "$$getFromFile$$"):
        password = open(os.getcwd() + '/server/DBPassword.txt', 'r').readline().rstrip()
    database.connect(address, username, password, database_name)


def disconnect():
    database.disconnect()


def setup_database():
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
    global objects_table_name, object_groups_table_name
    objects_table_name = 'OBJECTS_' + date.today().strftime("%Y%m%d") + '_' + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][0])
    object_groups_table_name = 'OBJECT_GROUPS_' + date.today().strftime("%Y%m%d") + '_' + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][0])
    if not database.does_table_exist(objects_table_name):
        database.execute('CREATE TABLE ' + objects_table_name + ' (ID int NOT NULL AUTO_INCREMENT, POS_X int NOT NULL,'
                                                                ' POS_Y int NOT NULL, OBJECT_TYPE varchar(64), TIME '
                                                                'timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, '
                                                                'PRIMARY KEY (ID))')  # OBJECT_TYPE: varchar ===> enum
    if not database.does_table_exist(object_groups_table_name):
        # TODO WIP
        database.execute(
            'CREATE TABLE ' + object_groups_table_name + ' (ID int NOT NULL AUTO_INCREMENT, PRIMARY KEY (ID))')
    # update run_count
    database.execute("UPDATE GENERAL SET VALUE = '" + str(
        int(database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][
                0]) + 1) + "' WHERE NAME='run_count'")


def clean():  # clean data from previous runs
    tables = database.fetch("SHOW TABLES")
    for table in tables:
        if table[0].startswith('RAW_DATA_') or table[0].startswith('OBJECTS_') or table[0].startswith('OBJECT_GROUPS_'):
            database.execute("DROP TABLE " + table[0])
    if database.does_table_exist('GENERAL'):
        database.execute("UPDATE GENERAL SET VALUE = '0' WHERE NAME='run_count' OR NAME='raw_data_table_count'")


def create_raw_data_table():
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
                                                ' POS_Y int NOT NULL, ANGLE int NOT NULL, DISTANCE_S1 int, '
                                                'DISTANCE_S2 int, SENSOR_TYPE enum("S1.US;S2.US", "S1.IR;S2.IR", '
                                                '"S1.US;S2.IR", "S1.IR;S2.US", "S1.US", "S1.IR", "S2.US", '
                                                '"S2.IR", "S3.US") NOT NULL, TIME timestamp NOT'
                                                ' NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (ID))')


def write_raw_data(pos_x: int, pos_y: int, angle: int, sensor_type: str, distance_s1=-1, distance_s2=-1):
    if distance_s1 == distance_s2 == -1:
        raise Exception("no value given")
    database.execute(
        "INSERT INTO " + raw_data_table_name + " (POS_X, POS_Y, ANGLE, DISTANCE_S1, DISTANCE_S2, SENSOR_TYPE) VALUES ("
        + str(pos_x) + ", " + str(pos_y) + ", " + str(angle) + ", " + str(distance_s1) + ", " + str(
            distance_s2) + ", '" + sensor_type + "')")
    # TODO might result in errors; testing required
    # create a new table to save resources after 10000 (or maybe more) entries have been written
    if count_raw_data_entries() > 10000:
        analysis_algorithms.complete_primary_analysis()
        create_raw_data_table()
        analysis_algorithms.thread0.current_id = 1
        analysis_algorithms.start()


def get_raw_data(entry_id: int):
    sql_statement = "SELECT POS_X, POS_Y, ANGLE, DISTANCE_S1, DISTANCE_S2, SENSOR_TYPE FROM " + raw_data_table_name + \
                    " WHERE ID=" + str(entry_id)
    return database.fetch(sql_statement)[0]


def count_raw_data_entries():
    return int(database.fetch("SELECT COUNT(ID) FROM " + raw_data_table_name)[0][0]) # TODO add lock


def write_object(pos_x: int, pos_y: int, object_type="undefined"):
    database.execute("INSERT INTO " + objects_table_name + " (POS_X, POS_Y, OBJECT_TYPE) VALUES (" + str(pos_x) +
                     ", " + str(pos_y) + ", '" + object_type + "')")


def get_object(entry_id: int):
    sql_statement = "SELECT POS_X, POS_Y, OBJECT_TYPE FROM " + objects_table_name + " WHERE ID=" + str(entry_id)
    return database.fetch(sql_statement)[0]


def count_object_entries():
    return int(database.fetch("SELECT COUNT(ID) FROM " + objects_table_name)[0][0])
