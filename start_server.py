#!/usr/bin/env python3
import socket
import sys

import mapping0
import mapping1
import server

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
    print('[start_server.py] some features might not work properly')
    mapping0.run()
elif program == 'mapping1':
    print('[start_server.py] some features might not work properly')
    mapping1.run()
else:
    raise Exception('[start_server.py] Program not found')
