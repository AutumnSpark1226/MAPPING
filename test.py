#!/usr/bin/env pybricks-micropython
# this script contains test code
import time

from pybricks.ev3devices import GyroSensor
from pybricks.ev3devices import Motor  # not found by PyCharm; pip install pybricks
from pybricks.ev3devices import UltrasonicSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port

ev3 = EV3Brick()
motor_a = Motor(Port.A)
gyro_s3 = GyroSensor(Port.S3)
ultrasonic_s1 = UltrasonicSensor(Port.S1)
ultrasonic_s2 = UltrasonicSensor(Port.S2)


def test1():
    motor_a.run_time(500, 2000)
    # Play another beep sound.
    ev3.speaker.beep(1000, 500)
    ev3.speaker.set_volume(1000)
    ev3.speaker.say("Jeremias: failure")
    # measure distance
    print("distance: " + str(ultrasonic_s1.distance()))


def calibrate():
    reset_angle()
    print('WIP')


def reset_angle():
    motor_a.reset_angle(0)
    gyro_s3.reset_angle(0)


def measure():
    # spam into the console
    if gyro_s3.angle() != motor_a.angle():
        print('WARNING: gyro sensors and motor angle not the same!')
        reset_angle()
    motor_a.run_angle(6, 360, wait=False)
    while gyro_s3.angle() < 360:
        if motor_a.angle >= 360:
            print('ERROR: sensor error! (motor_a.angle() >= 360)')
        distance_s1 = ultrasonic_s1.distance()
        distance_s2 = ultrasonic_s2.distance()
        angle_s3 = gyro_s3.angle()
        angle_a = motor_a.angle()
        print('sensors 1: ' + str(distance_s1))
        print('sensors 2: ' + str(distance_s2))
        print('gyro' + str(angle_s3))
        print('motor A' + str(angle_a))
        time.sleep(0.1)


def test_for_ultrasonic_interferences():
    print('S1')
    print(ultrasonic_s1.presence())
    print(ultrasonic_s1.distance())
    ultrasonic_s2.distance(silent=True)
    print(ultrasonic_s1.presence())
    print(ultrasonic_s1.distance())
    time.sleep(0.5)
    print('S2')
    ultrasonic_s2.distance()
    print(ultrasonic_s2.presence())
    print(ultrasonic_s2.distance())
    ultrasonic_s1.distance(silent=True)
    print(ultrasonic_s2.presence())
    print(ultrasonic_s2.distance())
    ultrasonic_s1.distance()


if __name__ == '__main__':
    calibrate()
    measure()
