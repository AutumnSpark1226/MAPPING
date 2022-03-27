#!/usr/bin/env python

import socket
import threading
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
        print(self.thread_name + ' initialized')

    def run(self):
        # save connections of the robots to the variables (They are separated by their hostnames.)
        server.start(6666)
        print('server started')
        while True:
            con, address = server.accept_client()
            print('connection request (' + str(address) + ')')
            address = socket.gethostbyaddr(address[0])[0]  # get hostname
            if address == 'mapping0':
                global mapping0_connection
                mapping0_connection = con
                print(address + ' connected')
            elif address == 'mapping1':
                global mapping1_connection
                mapping1_connection = con
                print(address + ' connected')
            else:
                con.close()
                print(address + ' tried to connect')
            while mapping0_connection and mapping1_connection:
                # sleep while both robots are connected
                sleep(2)


def start():
    global ev3_connect_thread
    ev3_connect_thread = EV3Connect()
    ev3_connect_thread.start()
    password = open('DBPassword.txt', 'r').read()
    database.connect('localhost', 'MAPPING_server', password, 'MAPPING')
    print('connected to database')
    wait_for_connections()
    print('all clients connected')
    while True:
        print('WIP')  # TODO WIP
        break


def wait_for_connections():
    while not (mapping0_connection and mapping1_connection):
        sleep(0.5)


if __name__ == '__main__':
    start()
