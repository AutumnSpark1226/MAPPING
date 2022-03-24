#!/usr/bin/env pybricks-micropython
from resources.communication import client


def start():
    client.connect('server', 6666)


if __name__ == '__main__':
    start()
