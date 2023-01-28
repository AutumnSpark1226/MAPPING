#!/usr/bin/env pybricks-micropython
import sys
from time import sleep

sys.path.insert(0, "/home/home/MAPPING")

from pybricks.hubs import EV3Brick
from lib.communication import client

ev3 = EV3Brick()
distance_sensor_type = "S3.US"
# TODO initialize motors


def drive_forward(cm: int):
    if ultrasonic.distance() + 100 >= cm * 10:
        client.send_text("objectNearby")
        client.send_text(distance_sensor_type)
        client.send_text(ultrasonic.distance())
        client.send_text(gyro.angle())
    else:
        degrees = cm * 21.17647058823529
        engineA.run_angle(90, degrees)
        client.send_text("ok")


def rotate(degrees: int):
    climberB.run_angle(90, 360)
    rotatorC.run_angle(30, degrees)
    climberB.run_angle(90, -360)
    client.send_text("ok")


def start():
    host = open('/home/robot/MAPPING/host.txt', 'r').readline().rstrip()
    print("[mapping1/main.py] connecting...")
    client.connect(host, 6666)  # ip
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
    ev3.speaker.beep(duration=1000)
    while True:
        command = client.receive_text()
        if command == 'drive_forward':
            drive_forward(int(client.receive_text()))
        elif command == 'exit':
            break
        elif command == 'rotate':
            rotate(int(client.receive_text()))
    stop()


if __name__ == '__main__':
    run()
