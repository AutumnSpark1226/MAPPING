#!/usr/bin/env python3
import sys
import socket
import threading
from time import sleep

import lib.communication.server as server
from lib import database

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
        #count = 0  # test purposes only
        while True:
            con, address = server.accept_client()
            hostname = socket.gethostbyaddr(address[0])[0]  # get hostname
            print('[server/main.py] connection request (' + hostname + ')')
            if hostname == 'mapping0':
            #if count == 0: # test purposes only
                #count = 1 # test purposes only
                global mapping0_connection
                mapping0_connection = con
                print('[server/main.py] ' + hostname + ' connected')
            elif hostname == 'mapping1':
            #elif count == 1: # test purposes only
                global mapping1_connection
                mapping1_connection = con
                print('[server/main.py] ' + hostname + ' connected')
            else:
                con[0].close()
                print('[server/main.py] ' + hostname + ' tried to connect')
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
    server.send_text(mapping0_connection, 'ready')
    server.send_text(mapping1_connection, 'ready')
    mapping0_ready = server.receive_text(mapping0_connection)
    mapping1_ready = server.receive_text(mapping1_connection)
    if not (mapping0_ready == 'ready' and mapping1_ready == 'ready'):
        print('[server/main.py] mapping0: ' + mapping0_ready)
        print('[server/main.py] mapping1: ' + mapping1_ready)
        raise Exception('[server/main.py] robots not ready')


def stop():
    server.send_text(mapping0_connection, 'exit')
    server.send_text(mapping1_connection, 'exit')
    server.stop()
    database.disconnect()
    # TODO stop ev3_connect_thread()


def run():
    print('[server/main.py] starting...')
    start()
    print('[server/main.py] ready')
    # TODO WIP
    stop()


if __name__ == '__main__':
    run()
