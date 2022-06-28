# easy access to the database
import os
from datetime import date

from lib import database


def connect():
    password = open(os.getcwd() + '/server/DBPassword.txt', 'r').readline().rstrip()
    database.connect('localhost', 'MAPPING_server', password, 'MAPPING')


def disconnect():
    database.disconnect()


def setup_database():
    if not database.does_table_exist('GENERAL'):
        database.execute(
            'CREATE TABLE GENERAL (ID int NOT NULL AUTO_INCREMENT, NAME varchar(100) NOT NULL, VALUE varchar(255), '
            'CHANGED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (ID))')
        database.execute("INSERT INTO GENERAL (NAME, VALUE) VALUES ('created', '-> CHANGED')")
        database.execute("INSERT INTO GENERAL (NAME, VALUE) VALUES ('run_count', '0')")
    table_suffix = '_' + date.today().strftime("%Y%m%d") + '_' + str(
        database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][0])
    database.execute("UPDATE GENERAL SET VALUE = '" + str(
        int(database.fetch("SELECT VALUE FROM GENERAL WHERE NAME='run_count'")[0][0]) + 1) + "' WHERE NAME='run_count'")
    if not database.does_table_exist('RAW_DATA' + table_suffix):
        database.execute(
            'CREATE TABLE RAW_DATA' + table_suffix + '(ID int NOT NULL AUTO_INCREMENT, POS_X int NOT NULL, POS_Y int '
                                                     'NOT NULL, ANGLE int, DISTANCE_S1 int, DISTANCE_S2 int, '
                                                     'TIME timestamp NOT NULL DEFAULT '
                                                     'CURRENT_TIMESTAMP, PRIMARY KEY (ID))')


def clean():
    tables = database.fetch("SHOW TABLES")
    for table in tables:
        if table[0].startswith('RAW_DATA_'):
            database.execute("DROP TABLE " + table[0])
    database.execute("UPDATE GENERAL SET VALUE = '0' WHERE NAME='run_count'")
