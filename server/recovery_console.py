#!/usr/bin/env python3

import os
import sys

import main

sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))])

from lib.communication import server
from lib import database as db
import db_operations


def log(content):
    print('[server/recovery_console.py] ' + content)


def exit_console():
    # disconnect from database
    try:
        db_operations.disconnect()
    except Exception as e:
        log("Database was not connected or disconnect failed")
        print(e)
    # disconnect from server
    try:
        server.stop()
    except Exception as e:
        log("Server did not start or stop failed")
        print(e)


def database(command="console"):
    if command == "console":
        while True:
            command = input("DB> ")
            if command == "exit" or command == "quit":
                break
            database(command)
    elif command == "connect":
        try:
            db_operations.connect()
        except Exception as e:
            log("Connecting to the database failed")
            print(e)
    elif command.startswith("connect "):
        command_parts = command.replace("connect '", "").split("' '")
        if len(command_parts) == 4:
            try:
                db_operations.connect(command_parts[0], command_parts[1], command_parts[2], command_parts[3])
            except Exception as e:
                log("Connecting to the database failed")
                print(e)
        else:
            log("Wrong number of arguments")
            log("Arguments must be separated by \\' \\'")
            log("Type 'help' for more information.")
    elif command == "disconnect":
        try:
            db_operations.disconnect()
        except Exception as e:
            log("Database was not connected or disconnect failed")
            print(e)
    elif command == "setup":
        try:
            db_operations.setup_database()
        except Exception as e:
            log("Command failed")
            print(e)
    elif command == "clean":
        try:
            db_operations.clean()
        except Exception as e:
            log("Command failed")
            print(e)
    elif command == "reset":
        try:
            tables = db.fetch("SHOW TABLES")
            for table in tables:
                db.execute("DROP TABLE " + table[0])
        except Exception as e:
            log("Command failed")
            print(e)
    elif command.startswith("execute "):
        try:
            db.execute(command.replace("execute ", ""))
        except Exception as e:
            log("Command failed")
            print(e)
    elif command.startswith("fetch "):
        try:
            print(db.fetch(command.replace("fetch ", "")))
        except Exception as e:
            log("Command failed")
            print(e)
    else:
        log("Command not found")
        log("Type 'help' for more information.")


def comm_server(command="console"):  # TODO add more commands
    if command == "console":
        while True:
            command = input("COMM_SERVER> ")
            if command == "exit" or command == "quit":
                break
            comm_server(command)
    elif command == "start":
        try:
            server.start(6666)
        except Exception as e:
            log("Command failed")
            print(e)
    elif command == "stop":
        try:
            server.stop()
        except Exception as e:
            log("Command failed")
            print(e)
    else:
        log("Command not found")
        log("Type 'help' for more information.")


def comm_client(command="console"):  # TODO add more commands
    if command == "console":
        while True:
            command = input("COMM_CLIENT> ")
            if command == "exit" or command == "quit":
                break
            comm_client(command)
    else:
        log("Command not found")
        log("Type 'help' for more information.")


if __name__ == '__main__':  # TODO add more commands
    mode = ""
    while True:
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            exit_console()
            break
        elif user_input.startswith("database"):
            if user_input.startswith("database "):
                database(user_input.replace("database ", ""))
            else:
                database()
        elif user_input.startswith("comm.server"):
            if user_input.startswith("comm.server "):
                comm_server(user_input.replace("comm.server ", ""))
            else:
                comm_server()
        elif user_input.startswith("comm.client"):
            if user_input.startswith("comm.client "):
                comm_client(user_input.replace("comm.client ", ""))
            else:
                comm_client()
        elif user_input == "server":
            main.run()
        else:
            log("Command not found")
            log("Type 'help' for more information.")
