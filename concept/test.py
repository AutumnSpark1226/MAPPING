#!/usr/bin/env pybricks-micropython

# this script contains test code
import time

from pybricks.ev3devices import Motor  # not found by PyCharm; working
from pybricks.ev3devices import TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Color, Port

ev3 = EV3Brick()
engineA = Motor(Port.A)
climberB = Motor(Port.B)
rotatorC = Motor(Port.C)
# gyro_s3 = GyroSensor(Port.S3)
# ultrasonic_s1 = TouchSensor(Port.S1)
ultrasonic_s1_error_correction = 0
# ultrasonic_s2 = UltrasonicSensor(Port.S2)
ultrasonic_s2_error_correction = 0


def test1():
    # motor_a.run_time(500, 2000)
    ev3.speaker.beep(1000, 500)
    ev3.speaker.set_volume(100)
    ev3.speaker.say("Justus is dumb as fuck! you lost!")
    # measure distance
    # print("distance 1: " + str(ultrasonic_s1.distance()))
    # print("distance 2: " + str(ultrasonic_s2.distance()))


def test2():
    i = 0
    ev3.light.on(Color.RED)
    ev3.speaker.say("You suck!")
    ev3.screen.print(str(ev3.screen.width) + " " + str(ev3.screen.height))
    ts = TouchSensor(Port.S1)
    while True:
        ev3.screen.print(i)
        if ts.pressed():
            ev3.speaker.say("true")
            time.sleep(1)
            break
        else:
            ev3.speaker.say("false")
        time.sleep(1)
        i += 1
    time.sleep(5)


def rotate(degrees):
    climberB.run_angle(90, 360)
    rotatorC.run_angle(30, degrees)
    climberB.run_angle(90, -360)
    ev3.speaker.say("Rotated 90 degrees!")


def drive(cm):
    degrees = cm * 21.17647058823529
    engineA.run_angle(90, degrees)
    ev3.speaker.say(cm)


def auto_calibrate():
    reset_angle()
    print('WIP')


def advanced_calibrate(real_distance_s1, real_distance_s2):
    print("Do NOT move the ultrasonic sensors!")
    global ultrasonic_s1_error_correction, ultrasonic_s2_error_correction
    ultrasonic_s1_error_correction = get_error_correction(ultrasonic_s1, real_distance_s1)
    ultrasonic_s2_error_correction = get_error_correction(ultrasonic_s2, real_distance_s2)


def reset_angle():
    motor_a.reset_angle(0)
    gyro_s3.reset_angle(0)


def get_error_correction(ultrasonic_sensor, real_distance):
    calibrated_value = ultrasonic_sensor.distance()
    for i in range(20):
        calibrated_value = (calibrated_value + ultrasonic_sensor.distance()) / 2
    return real_distance - int(calibrated_value)


def measure():
    # spam into the console
    if gyro_s3.angle() != motor_a.angle():
        print('WARNING: gyro sensors and motor angle not the same!')
        reset_angle()
    while gyro_s3.angle() < 360:
        if motor_a.angle >= 361:
            print('ERROR: sensor error! (motor_a.angle() >= 361)')
        motor_a.run_angle(6, 1)
        distance_s1 = ultrasonic_s1.distance() + ultrasonic_s1_error_correction
        distance_s2 = ultrasonic_s2.distance() + ultrasonic_s2_error_correction
        angle_s3 = gyro_s3.angle()
        angle_a = motor_a.angle()
        print('sensor S1: ' + str(distance_s1))
        print('sensor S2: ' + str(distance_s2))
        print('gyro S3: ' + str(angle_s3))
        print('motor A: ' + str(angle_a))


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
    rotate(90)
    drive(20)
