#!/usr/bin/env python3
import os
import sys
import threading
from time import sleep

sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))])

import lib.communication.server as server
import db_operations
import analysis_algorithms


class EV3Connect(threading.Thread):
    """
    create a new thread handling the connection process
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_name = 'EV3ConnectThread'
        print('[server/main.py] ' + self.thread_name + ' initialized')

    def run(self):
        # save connections of the robots
        server.start(6666)
        print('[server/main.py] server started')
        while True:
            con, address = server.accept_client()
            client_id = server.receive_text(con)
            print('[server/main.py] connection request (' + client_id + ')')
            if client_id == 'mapping0':
                global mapping0_connection
                mapping0_connection = con
                print('[server/main.py] ' + client_id + ' connected')
            elif client_id == 'mapping1':
                global mapping1_connection
                mapping1_connection = con
                print('[server/main.py] ' + client_id + ' connected')
            else:
                con.close()
                print('[server/main.py] ' + client_id + ' tried to connect')
                sleep(0.5)
            # yes, this is a security risk
            # TODO find a better way to verify the client

    def stop(self):
        if self.is_alive():
            os.system('kill ' + str(self.native_id))  # easiest way to stop the thread (kills the entire process)


ev3_connect_thread = EV3Connect()
mapping0_connection = None
mapping1_connection = None
failure_count = 0
max_failures = 10

robot_position_x = 0
robot_position_y = 0


def start():
    db_operations.connect()
    db_operations.clean()  # TODO only clean in specific situations
    db_operations.setup_database()
    print('[server/main.py] database ready')
    ev3_connect_thread.start()
    # wait til the robots are both connected
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
    analysis_algorithms.start()


def stop():
    server.send_text(mapping0_connection, 'exit')
    server.send_text(mapping1_connection, 'exit')
    server.stop()
    print('[server/main.py] server stopped')
    analysis_algorithms.stop()
    print('[server/main.py] analysis_algorithms stopped')
    db_operations.disconnect()
    print('[server/main.py] disconnected from database')
    print('[server/main.py] killing remaining threads')
    # last to stop (kills the process)
    ev3_connect_thread.stop()


def wait_for_connections():
    while not (mapping0_connection and mapping1_connection):
        sleep(0.5)


def validate_position():
    position_validity = True
    print("WIP")
    if not position_validity:
        recover_position()


def recover_position():
    recovery_successful = False
    print("WIP")
    if not recovery_successful:
        print("Position could not be recovered! The process will terminate")
        stop()


def drive_forward(cm: int):
    server.send_text(mapping1_connection, "drive_forward")
    server.send_text(mapping1_connection, str(cm))
    if server.receive_text(mapping1_connection) != "ok":
        global failure_count
        if failure_count >= max_failures:
            raise Exception("Too many failures occurred during driving")
        else:
            failure_count += 1
            drive_forward(cm)


def measure_at_current_location():
    server.send_text(mapping0_connection, "measure_at_current_location")
    if server.receive_text(mapping0_connection) != "ok":
        global failure_count
        if failure_count >= max_failures:
            raise Exception("Too many failures occurred during measurement")
        else:
            failure_count += 1
            measure_at_current_location()
    response = server.receive_text(mapping0_connection)
    while response != "finished":
        angle = response
        distance_s1 = server.receive_text(mapping0_connection)
        distance_s2 = server.receive_text(mapping0_connection)
        db_operations.write_raw_data(robot_position_x, robot_position_y, angle, distance_s1, distance_s2)


def run():
    print('[server/main.py] starting...')
    start()
    print('[server/main.py] ready')
    while True:
        validate_position()
        # TODO create the map
        break  # temporary solution to prevent an endless loop
    print('[server/main.py] shutdown')
    stop()


if __name__ == '__main__':
    run()
