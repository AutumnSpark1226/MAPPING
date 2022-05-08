#!/usr/bin/env python3
import socket
import sys

import mapping1
import server
import mapping0

host = socket.gethostname()
program = '?'
if len(sys.argv) == 2:
    program = sys.argv[1]
elif host == 'laptop':
    program = 'server'
elif host == 'mapping0':
    program = 'mapping0'
elif host == 'mapping1':
    program = 'mapping1'
else:
    program = input('Choose a program [server, mapping0, mapping1]: ')
if program == 'server':
    server.run()
elif program == 'mapping0':
    mapping0.run()
elif program == 'mapping1':
    mapping1.run()
else:
    raise Exception('[start.py] Program not found')
