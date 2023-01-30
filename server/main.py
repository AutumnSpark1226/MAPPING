#!/usr/bin/env python3
import os
import sys
import threading
from shlex import quote as shlex_quote
from socket import socket
from time import sleep

sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))])

import lib.communication.server as server
import db_operations
import analysis_algorithms
import driving_algorythm



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
        global mapping0_connection, mapping0_initialized, mapping1_connection, mapping1_initialized
        while True:
          if mapping0_initialized and mapping1_initialized:
            # TODO periodically check if the clients are still available
          else:
            con, address = server.accept_client()
            # yes, this is a security risk  
            # TODO find a better way to verify the client
            client_id = server.receive_text(con)
            print('[server/main.py] connection request (' + client_id + ')')
            if client_id == 'mapping0':
                mapping0_connection = con
                mapping0_initialized = True
                print('[server/main.py] ' + client_id + ' connected')
            elif client_id == 'mapping1':
                mapping1_connection = con
                mapping1_initialized = True
                print('[server/main.py] ' + client_id + ' connected')
            else:
                con.close()
                print('[server/main.py] ' + client_id + ' tried to connect')
                sleep(0.5)

    def stop(self):
        if self.is_alive():
            os.system(shlex_quote('kill ' + str(self.native_id)))  # easiest way to stop the thread (kills the entire
            # process)
            
            
ev3_connect_thread = EV3Connect()
mapping0_connection: socket
mapping0_initialized = False
mapping1_connection: socket
mapping1_initialized = False
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
    analysis_algorithms.stop()
    db_operations.disconnect()
    # last to stop (kills the process)
    ev3_connect_thread.stop()


def wait_for_connections():
    while not (mapping0_initialized and mapping1_initialized):
        sleep(0.5)


def validate_position():
    position_validity = True
    print("validate_position WIP")
    if not position_validity:
        recover_position()


def recover_position():
    recovery_successful = False
    print("recover_position WIP")
    if not recovery_successful:
        print("Position could not be recovered! The process will terminate")
        stop()


def drive_forward(mm: int):
    server.send_text(mapping1_connection, "drive_forward")
    server.send_text(mapping1_connection, str(mm))
    response = server.receive_text(mapping1_connection)
    if response == "ok":
        # TODO calculate new position
        print("")
    elif response == "objectNearby":
        sensor_type = server.receive_text(mapping1_connection)
        distance = server.receive_text(mapping1_connection)
        angle = server.receive_text(mapping1_connection)
        db_operations.lock_raw_data_table()
        db_operations.write_raw_data(robot_position_x, robot_position_y, angle, sensor_type, distance_s1=distance)
        db_operations.unlock_raw_data_table()
    else:
        global failure_count
        if failure_count >= max_failures:
            raise Exception("Too many failures occurred during driving")
        else:
            failure_count += 1
            validate_position()
            drive_forward(mm)
    driving_algorythm.change_position(mm)


def measure_at_current_location():
    db_operations.lock_raw_data_table()
    server.send_text(mapping0_connection, "measure_at_current_location")
    if server.receive_text(mapping0_connection) != "ok":
        global failure_count
        if failure_count >= max_failures:
            raise Exception("Too many failures occurred during measurement")
        else:
            validate_position()
            failure_count += 1
            measure_at_current_location()
    sensor_type = server.receive_text(mapping0_connection)
    response = server.receive_text(mapping0_connection)
    while response != "finished":
        angle = response
        distance_s1 = server.receive_text(mapping0_connection)
        distance_s2 = server.receive_text(mapping0_connection)
        db_operations.write_raw_data(robot_position_x, robot_position_y, angle, sensor_type, distance_s1=distance_s1,
                                     distance_s2=distance_s2)
        server.send_text(mapping0_connection, "ok")
        response = server.receive_text(mapping0_connection)
    db_operations.unlock_raw_data_table()


def rotate(angle: int):
    server.send_text(mapping1_connection, "rotate")
    server.send_text(mapping1_connection, str(angle))
    response = server.receive_text(mapping1_connection)
    if response == "ok":
        print("")
    else:
        global failure_count
        if failure_count >= max_failures:
            raise Exception("Too many failures occurred during rotating")
        else:
            failure_count += 1
            validate_position()
            rotate(angle)
    driving_algorythm.change_rotation(angle)


def run():
    print('[server/main.py] starting...')
    start()
    print('[server/main.py] ready')
    validate_position()
    measure_at_current_location()
    # TODO create the map
    print('[server/main.py] shutdown')
    stop()


if __name__ == '__main__':
    run()
