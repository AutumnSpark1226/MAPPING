#!/usr/bin/env pybricks-micropython
import os
import sys
from time import sleep

#sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))])

from pybricks.hubs import EV3Brick

from lib.communication import client

ev3 = EV3Brick()


def drive_forward(length):
    print('WIP')


def start():
    print("[mapping1/main.py] connecting")
    client.connect('laptop', 6666)
    print("[mapping1/main.py] connected")
    while client.receive_text() != 'ready':
        sleep(0.5)
    client.send_text('ready')
    ev3.speaker.beep(duration=1000)


def run():
    print("[mapping1/main.py] starting")
    start()
    print("[mapping1/main.py] ready")
    while True:
        command = client.receive_text()
        if command == 'drive_forward':
            drive_forward(int(client.receive_text()))
        elif command == 'exit':
            break
    client.disconnect()


if __name__ == '__main__':
    run()
