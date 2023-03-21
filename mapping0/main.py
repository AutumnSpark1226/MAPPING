#!/usr/bin/env pybricks-micropython
import os
import sys
from time import sleep

from pybricks.ev3devices import InfraredSensor, GyroSensor, UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port

working_dir = os.getcwd()
sys.path.insert(0, working_dir)

from lib.communication import client

ev3 = EV3Brick()
ultrasonic_s1 = UltrasonicSensor(Port.S1)
infrared_s2 = InfraredSensor(Port.S2)
gyro_s3 = GyroSensor(Port.S3)

distance_sensor_type = "S1.US,S2.IR"


def measure():
    client.send_text("ok")
    client.send_text(distance_sensor_type)
    for i in range(0, 10):
        # measure
        degrees = gyro_s3.angle()
        s1_value = ultrasonic_s1.distance()
        s2_value = infrared_s2.distance()
        client.send_text(str(degrees))
        client.send_text(str(s1_value))
        client.send_text(str(s2_value))
        if not client.receive_text() == "ok":
            raise Exception("Error (server did not respond correctly)")
    client.send_text("finished")


def start():
    host = open('/home/robot/MAPPING/host.txt', 'r').readline().rstrip()  # TODO use relative path
    print("[mapping0/main.py] connecting...")
    client.connect(host, 6666)
    print("[mapping0/main.py] connected")
    client.send_text("mapping0")
    while client.receive_text() != 'ready':
        sleep(0.5)
    client.send_text('ready')


def stop():
    client.disconnect()
    print("[mapping0/main.py] disconnected")


def run():
    print("[mapping0/main.py] starting")
    start()
    print("[mapping0/main.py] ready")
    while True:
        command = client.receive_text()
        if command == 'measure':
            measure()
        elif command == 'exit':
            break
    stop()


if __name__ == '__main__':
    run()
