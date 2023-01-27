#!/usr/bin/env pybricks-micropython
import os
import sys
from time import sleep

sys.path.insert(0, "/home/robot/MAPPING")

from pybricks.hubs import EV3Brick
from lib.communication import client

ev3 = EV3Brick()
distance_sensor_type = "S1.US;S2.US"


def measure_at_current_location():
    # send dummy values
    client.send_text("ok")
    client.send_text(distance_sensor_type)
    client.send_text("0")
    client.send_text("200")
    client.send_text("2550")
    client.send_text("finished")


def start():
    host = open('/home/robot/MAPPING/host.txt', 'r').readline().rstrip()
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
    ev3.speaker.beep(duration=1000)
    while True:
        command = client.receive_text()
        if command == 'measure_at_current_location':
            measure_at_current_location()
        elif command == 'exit':
            break
    stop()


if __name__ == '__main__':
    run()
