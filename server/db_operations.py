# easy access to the database
import os
from datetime import date

from lib import database

raw_data_table_suffix = "???"


def connect(address="localhost", username="MAPPING_server", password="getFromFile", database_name='MAPPING'):
    if password == "getFromFile":
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
    # set raw_data_table_suffix
    global raw_data_table_suffix
    raw_data_table_suffix = '_' + date.today().strftime("%Y%m%d") + '_' + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][0]) + "_" + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='raw_data_table_count'")[0][0])
    # update run_count and raw_data_table_suffix
    database.execute("UPDATE GENERAL SET VALUE = '" + str(
        int(database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][
                0]) + 1) + "' WHERE NAME='run_count'")
    database.execute("UPDATE GENERAL SET VALUE = '" + str(
        int(database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='raw_data_table_count'")[0][
                0]) + 1) + "' WHERE NAME='raw_data_table_count'")
    # create raw data table
    if not database.does_table_exist('RAW_DATA' + raw_data_table_suffix):
        database.execute(
            'CREATE TABLE RAW_DATA' + raw_data_table_suffix + ' (ID int NOT NULL AUTO_INCREMENT, POS_X int NOT NULL,'
                                                              ' POS_Y int NOT NULL, ANGLE int, DISTANCE_S1 int, '
                                                              'DISTANCE_S2 int, TIME timestamp NOT NULL DEFAULT '
                                                              'CURRENT_TIMESTAMP, PRIMARY KEY (ID))')


def clean():
    tables = database.fetch("SHOW TABLES")
    for table in tables:
        if table[0].startswith('RAW_DATA_'):
            database.execute("DROP TABLE " + table[0])
    database.execute("UPDATE GENERAL SET VALUE = '0' WHERE NAME='run_count'")
    database.execute("UPDATE GENERAL SET VALUE = '0' WHERE NAME='raw_data_table_count'")


def write_raw_data(pos_x, pos_y, angle, distance_s1, distance_s2):
    database.execute(
        "INSERT INTO RAW_DATA" + raw_data_table_suffix + " (POS_X, POS_Y, ANGLE, DISTANCE_S1, DISTANCE_S2) VALUES ("
        + pos_x + ", " + pos_y + ", " + angle + ", " + distance_s1 + ", " + distance_s2 + ")")


def get_raw_data(pos_x, pos_y, angle=-1024):
    sql_statement = "SELECT ID, ANGLE, DISTANCE_S1, DISTANCE_S2 FROM RAW_DATA" + raw_data_table_suffix + \
                    " WHERE POS_X=" + pos_x + " AND POS_Y=" + pos_y
    if angle != -1024:
        sql_statement += " AND ANGLE=" + str(angle)
    return database.fetch(sql_statement)
