#!/usr/bin/env pybricks-micropython

"""
print *.err.log files on the ev3's screen
no print() command because it would create another *.err.log file
"""


import os
import time

from pybricks.hubs import EV3Brick
from pybricks.parameters import Button

ev3 = EV3Brick()
max_lines_on_screen = 5  # TODO hardcode or calculate the value
max_chars_per_line = 25  # TODO hardcode or calculate the value


def choose_logfile():
    directory = "/home/robot/MAPPING"
    logfiles = scan_directory(directory)
    chosen_file = None
    cursor_position = 0
    while not chosen_file:
        if len(logfiles) <= max_lines_on_screen:
            loop_end = len(logfiles)
        else:
            loop_end = max_lines_on_screen
        ev3.screen.clear()
        for i in range(loop_end):
            text_to_print = logfiles[i].replace(directory, ".")
            if i == cursor_position:
                text_to_print = "> " + text_to_print
            ev3.screen.print(text_to_print)
        pressed_button = ev3.buttons.pressed()
        while not len(pressed_button) == 1:
            pressed_button = ev3.buttons.pressed()
            time.sleep(1)
        if pressed_button[0] == Button.CENTER:
            chosen_file = logfiles[cursor_position]
        elif pressed_button[0] == Button.DOWN:
            cursor_position += 1
        elif pressed_button[0] == Button.UP:
            cursor_position -= 1
        if cursor_position > len(logfiles):
            cursor_position = len(logfiles)
        elif cursor_position < 0:
            cursor_position = 0
    return open(chosen_file)


def scan_directory(directory: str):
    logfiles = []
    scan_result = os.listdir(directory)
    for entry in scan_result:
        if entry.endswith(".err.log"):
            logfiles.extend([directory + "/" + entry.name])
        #elif entry.is_dir():
        #    logfiles.extend(scan_directory(directory + "/" + entry.name))
    logfiles.sort()
    print("logfiles scanned")
    return logfiles


def print_logfile(lines: list[str], part: int):
    ev3.screen.clear()
    i = part * max_lines_on_screen
    loop_end = i + 10
    if loop_end > len(lines):
        loop_end = len(lines)
    while i < loop_end:
        ev3.screen.print(lines[i])
        i += 1


def interactive_logreader():
    logfile = choose_logfile()
    print("logfile chosen")
    logfile_position = 0
    line = logfile.readline()
    lines = []
    while line:
        add = [line.rstrip()[i: i + max_chars_per_line] for i in
               range(0, len(line.rstrip()), max_chars_per_line)]
        lines.extend(add)
        line = logfile.readline()
    lines_count = len(lines)
    while True:
        print_logfile(lines, logfile_position)
        pressed_button = ev3.buttons.pressed()
        while not len(pressed_button) == 1:
            pressed_button = ev3.buttons.pressed()
        if pressed_button[0] == Button.LEFT_UP:
            break
        elif pressed_button[0] == Button.DOWN:
            logfile_position += 1
        elif pressed_button[0] == Button.UP:
            logfile_position -= 1
        if logfile_position > lines_count:
            logfile_position = lines_count
        elif logfile_position < 0:
            logfile_position = 0
        time.sleep(3)


if __name__ == '__main__':
    interactive_logreader()
