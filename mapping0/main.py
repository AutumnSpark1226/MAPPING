#!/usr/bin/env pybricks-micropython
from time import sleep

from lib.communication import client


def measure_at_current_location():
    print('WIP')


def start():
    print("[mapping0/main.py] connecting")
    client.connect('laptop', 6666)
    print("[mapping0/main.py] connected")
    while client.receive_text() != 'ready':
        sleep(0.5)
    client.send_text('ready')


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
