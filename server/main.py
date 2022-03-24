#!/usr/bin/env python
import threading
import socket
from time import sleep

import resources.communication.server as server

ev3_connect_thread = None
mapping0_connection = None
mapping1_connection = None


class EV3Connect(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'EV3ConnectThread'
        print(self.thread_name + ' initialized')

    def run(self):
        server.start(6666)
        print('server started')
        while True:
            con, address = server.accept_client()
            print('connection request (' + str(address) + ')')
            address = socket.gethostbyaddr(address[0])[0]
            if address == 'localhost':
                global mapping0_connection
                mapping0_connection = con
                print(address + ' connected')
            elif address == 'localhost':
                global mapping1_connection
                mapping1_connection = con
                print(address + ' connected')
            else:
                con.close()
                print(address + ' tried to connect')


def start():
    global ev3_connect_thread
    ev3_connect_thread = EV3Connect()
    ev3_connect_thread.start()
    # connect to database WIP

    wait_for_connections()
    print('all clients connected')
    while True:
        print('WIP')
        break


def wait_for_connections():
    while not (mapping0_connection and mapping1_connection):
        sleep(0.5)


if __name__ == '__main__':
    start()
