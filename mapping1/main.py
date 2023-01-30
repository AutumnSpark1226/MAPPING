#!/usr/bin/env pybricks-micropython
import sys
from time import sleep

sys.path.insert(0, "/home/robot/MAPPING")

from pybricks.hubs import EV3Brick
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
        client.send_text(gyro.angle())
    else:
        # TODO object check during driving
        degrees = mm * 211.7647058823529
        engine.run_angle(90, degrees)
        client.send_text("ok")


def rotate(degrees: int):
    climber.run_angle(90, 360)
    rotator.run_angle(30, degrees)
    climber.run_angle(90, -360)
    client.send_text("ok")


def start():
    host = open('/home/robot/MAPPING/host.txt', 'r').readline().rstrip()
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


def run():
    print("[mapping1/main.py] starting")
    start()
    print("[mapping1/main.py] ready")
    while True:
        command = client.receive_text()
        if command == 'drive_forward':
            drive_forward(int(client.receive_text()))
        elif command == 'rotate':
            rotate(int(client.receive_text()))
        elif command == 'exit':
            break
    stop()


if __name__ == '__main__':
    run()
