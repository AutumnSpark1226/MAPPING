#!/usr/bin/env python3
import os
import sys
import threading
from time import sleep

sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))])

import lib.communication.server as server
import db_operations


class EV3Connect(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'EV3ConnectThread'
        print('[server/main.py] ' + self.thread_name + ' initialized')

    def run(self):
        # save connections of the robots
        server.start(6666)
        print('[server/main.py] server started')
        # count = 0  # test purposes only
        while True:
            con, address = server.accept_client()
            id = server.receive_text(con)
            print('[server/main.py] connection request (' + id + ')')
            if id == 'mapping0':
                # if count == 0: # test purposes only
                # count = 1 # test purposes only
                global mapping0_connection
                mapping0_connection = con
                print('[server/main.py] ' + id + ' connected')
            elif id == 'mapping1':
                # elif count == 1: # test purposes only
                global mapping1_connection
                mapping1_connection = con
                print('[server/main.py] ' + id + ' connected')
            else:
                con.close()
                print('[server/main.py] ' + id + ' tried to connect')
                sleep(0.5)

    def stop(self):
        if self.is_alive():
            os.system('kill ' + str(self.native_id))  # easiest way to stop the thread (kills the entire process)


ev3_connect_thread = EV3Connect()
mapping0_connection = None
mapping1_connection = None
failure_count = 0


def start():
    db_operations.connect()
    db_operations.clean()  # TODO only clean in specific situations
    db_operations.setup_database()
    print('[server/main.py] database ready')
    global ev3_connect_thread
    ev3_connect_thread.start()
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
    # last to stop (kills the process)
    ev3_connect_thread.stop()


def wait_for_connections():
    while not (mapping0_connection and mapping1_connection):
        sleep(0.5)


def drive_forward(cm):
    server.send_text(mapping1_connection, "drive_forward")
    server.send_text(mapping1_connection, str(cm))
    if server.receive_text(mapping1_connection) != "ok":
        global failure_count
        if failure_count > 10:
            raise Exception("Too many failures to drive forward")
        else:
            failure_count += 1


def run():
    print('[server/main.py] starting...')
    start()
    print('[server/main.py] ready')
    # TODO WIP
    stop()


if __name__ == '__main__':
    run()
