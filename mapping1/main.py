#!/usr/bin/env python3
from time import sleep

from lib.communication import client


def drive_forward(length):
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
        if command == 'drive_forward':
            drive_forward(int(client.receive_text()))
        elif command == 'exit':
            break
    client.disconnect()


if __name__ == '__main__':
    run()
