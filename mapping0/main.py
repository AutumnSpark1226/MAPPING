#!/usr/bin/env pybricks-micropython
import os
import sys
from time import sleep

sys.path.insert(0, "/home/robot/MAPPING")

from pybricks.hubs import EV3Brick
from lib.communication import client

ev3 = EV3Brick()


def measure_at_current_location():
    print('WIP')


def start():
    print("[mapping0/main.py] connecting")
    client.connect('laptop', 6666)
    print("[mapping0/main.py] connected")
    while client.receive_text() != 'ready':
        sleep(0.5)
    client.send_text('ready')
    ev3.speaker.beep(duration=1000)


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
    client.disconnect()


if __name__ == '__main__':
    run()
