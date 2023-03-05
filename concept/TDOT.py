#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick

ev3 = EV3Brick()


def talk():
    ev3.speaker.set_volume(100)
    ev3.speaker.set_speech_options(language="de")
    ev3.speaker.say(
        "In unserem Projekt MAPPING haben wir uns zum Ziel gesetzt, einen Raum nicht nur in 2D zu scannen und visuell "
        "darzustellen, sondern auch einen Roboter in diesem Raum fahren zu lassen. Wir nutzen dafür die "
        "Programmiersprache Python. Zunächst werden wir den Raum mit Sensoren in 2D scannen und die Daten in Python "
        "eingelesen und verarbeitet. Mit diesen Daten werden wir dann einen Roboter ausstatten, der in der Lage ist, "
        "autonom durch den Raum zu fahren. Um den Roboter zu steuern, werden wir spezielle Algorithmen und "
        "Bewegungsabläufe programmieren. Der Roboter nutzt dann seine sensoren, um seine Position im Raum zu "
        "bestimmen und Hindernisse zu vermeiden.  Das Ergebnis ist ein vollautomatisches System, das es uns "
        "ermöglicht, einen Raum in 2D zu scannen und gleichzeitig einen Roboter darin zu bewegen. Diese Technologie "
        "hat viele Anwendungsbereiche, wie zum Beispiel in der Logistik, wo Roboter verwendet werden können, "
        "um Waren in Lagerhallen zu transportieren.")


if __name__ == "__main__":
    talk()
