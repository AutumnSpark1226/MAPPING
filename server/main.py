#!/usr/bin/env python
import socket
import threading
from datetime import datetime
from time import sleep

import resources.communication.server as server
from resources import database

ev3_connect_thread = None
mapping0_connection = None
mapping1_connection = None


class EV3Connect(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'EV3ConnectThread'
        print('[server/main.py] ' + self.thread_name + ' initialized')

    def run(self):
        # save connections of the robots to the variables (They are separated by their hostnames.)
        server.start(6666)
        print('[server/main.py] server started')
        while True:
            con, address = server.accept_client()
            print('[server/main.py] connection request (' + str(address) + ')')
            address = socket.gethostbyaddr(address[0])[0]  # get hostname
            if address == 'mapping0':
                global mapping0_connection
                mapping0_connection = con
                print('[server/main.py] ' + address + ' connected')
            elif address == 'mapping1':
                global mapping1_connection
                mapping1_connection = con
                print('[server/main.py] ' + address + ' connected')
            else:
                con.close()
                print('[server/main.py] ' + address + ' tried to connect')
                sleep(0.5)


def wait_for_connections():
    while not (mapping0_connection and mapping1_connection):
        sleep(0.5)


def setup_database():
    if not database.does_table_exist('GENERAL'):
        database.execute(
            'CREATE TABLE GENERAL (ID int NOT NULL AUTO_INCREMENT, NAME varchar(100) NOT NULL, VALUE varchar(255), '
            'CHANGED timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (ID))')
        database.execute(
            "INSERT INTO GENERAL (NAME, VALUE) VALUES ('created', '-> CHANGED')")
        database.execute(
            "INSERT INTO GENERAL (NAME, VALUE) VALUES ('created', '-> CHANGED')")
        print("[server/main.py] created table 'GENERAL'")


def start():
    global ev3_connect_thread
    ev3_connect_thread = EV3Connect()
    ev3_connect_thread.start()
    password = open('DBPassword.txt', 'r').readline().rstrip()
    database.connect('localhost', 'MAPPING_server', password, 'MAPPING')
    print('[server/main.py] connected to database')
    setup_database()
    print('[server/main.py] database ready')
    wait_for_connections()
    print('[server/main.py] all clients connected')


def run():
    print('[server/main.py] starting...')
    start()
    print('[server/main.py] ready')
    # TODO WIP


if __name__ == '__main__':
    run()
