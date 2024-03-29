#!/usr/bin/env pybricks-micropython
import os
import random
import sys
from time import sleep

working_dir = os.getcwd()
sys.path.insert(0, working_dir)

from pybricks.hubs import EV3Brick
from lib.communication import client

ev3 = EV3Brick()
distance_sensor_type = "S1.US,S2.IR"


def measure_at_current_location():
    # TODO use real sensors instead of dummy data
    # send dummy values
    client.send_text("ok")
    client.send_text(distance_sensor_type)
    for i in range(0, 10):
        client.send_text(str(random.randint(0, 360)))
        client.send_text(str(random.randint(0, 2550)))
        client.send_text(str(random.randint(0, 2550)))
        if not client.receive_text() == "ok":
            raise Exception("Error (server did not respond correctly)")
    client.send_text("finished")


def start():
    host = open(working_dir + '/host.txt', 'r').readline().rstrip()
    print("[mapping0/main.py] connecting...")
    client.connect(host, 6666)
    print("[mapping0/main.py] connected")
    client.send_text("mapping0")
    while client.receive_text() != 'ready':
        sleep(0.5)
    client.send_text('ready')


def stop():
    client.disconnect()
    print("[mapping0/main.py] disconnected")


def run():
    print("[mapping0/main.py] starting")
    start()
    print("[mapping0/main.py] ready")
    while True:
        command = client.receive_text()
        if command == 'measure_at_current_location':
            measure_at_current_location()
        elif command == 'exit':
            break
    stop()


if __name__ == '__main__':
    run()
