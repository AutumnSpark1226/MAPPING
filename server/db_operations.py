# easy access to the database
import os

from lib import database


def connect():
    password = open(os.getcwd() + '/server/DBPassword.txt', 'r').readline().rstrip()
    database.connect('localhost', 'MAPPING_server', password, 'MAPPING')
    setup_database()


def disconnect():
    database.disconnect()


def setup_database():
    if not database.does_table_exist('GENERAL'):
        database.execute(
            'CREATE TABLE GENERAL (ID int NOT NULL AUTO_INCREMENT, NAME varchar(100) NOT NULL, VALUE varchar(255), '
            'CHANGED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (ID))')
        database.execute("INSERT INTO GENERAL (NAME, VALUE) VALUES ('created', '-> CHANGED')")
