#!/usr/bin/env pybricks-micropython
import os
import sys
from time import sleep

from pybricks.hubs import EV3Brick

working_dir = os.getcwd()
sys.path.insert(0, working_dir)

from lib.communication import client

ev3 = EV3Brick()
# TODO initialize motors and sensors

ultrasonic = None
gyro = None
engine = None
climber = None
rotator = None

distance_sensor_type = "S3.US"


def drive_forward(mm: int):
    if ultrasonic.distance() + 100 >= mm:
        client.send_text("objectNearby")
        client.send_text(distance_sensor_type)
        client.send_text(ultrasonic.distance())
        client.send_text(gyro.degrees())
    else:
        # TODO object check during driving
        degrees = mm * 211.7647058823529
        engine.run_degrees(90, degrees)
        client.send_text("ok")


def rotate(degrees: int):
    climber.run_degrees(90, 360)
    rotator.run_degrees(30, degrees)
    climber.run_degrees(90, -360)
    client.send_text("ok")


def start():
    host = open('./host.txt', 'r').readline().rstrip()  # TODO add relative path
    print("[mapping1/main.py] connecting...")
    client.connect(host, 6666)
    print("[mapping1/main.py] connected")
    client.send_text("mapping1")
    while client.receive_text() != 'ready':
        sleep(0.5)
    client.send_text('ready')


def stop():
    client.disconnect()
    print("[mapping1/main.py] disconnected")


def status_check():
    if ev3.battery.voltage() < 7000:
        client.send_text("batteryLow")
    else:
        client.send_text('ok')


def run():
    print("[mapping1/main.py] starting")
    start()
    print("[mapping1/main.py] ready")
    while True:
        command = client.receive_text()
        if command == 'status_check':
            status_check()
        elif command == 'drive_forward':
            drive_forward(int(client.receive_text()))
        elif command == 'rotate':
            rotate(int(client.receive_text()))
        elif command == 'exit':
            break
    stop()


if __name__ == '__main__':
    run()
