#!/usr/bin/env pybricks-micropython
import sys
from time import sleep

sys.path.insert(0, "/home/robot/MAPPING")

from pybricks.hubs import EV3Brick
from lib.communication import client

ev3 = EV3Brick()


def drive_forward(length):
    print('WIP')


def start():
    print("[mapping1/main.py] connecting")
    client.connect('192.168.0.2', 6666)  # ip
    print("[mapping1/main.py] connected")
    client.send_text("mapping1")
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
