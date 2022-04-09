#!/usr/bin/env python3
from time import sleep

from resources.communication import client


def measure_at_current_location():
    print('WIP')


def start():
    client.connect('server', 6666)
    while client.receive_text() != 'ready':
        sleep(0.5)
    client.send_text('ready')


def run():
    start()
    while True:
        command = client.receive_text()
        if command == 'measure_at_current_location':
            measure_at_current_location()
        elif command == 'exit':
            break
    client.disconnect()


if __name__ == '__main__':
    run()
