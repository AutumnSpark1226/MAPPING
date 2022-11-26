#!/usr/bin/env sh
HOSTNAME=$(cat /etc/hostname)
PROGRAM="?"
if [ "$#" -eq "1" ]; then
  PROGRAM=$1
else
  if [ "$HOSTNAME" = "laptop" ]; then
    PROGRAM="server"
  elif [ "$HOSTNAME" = "mapping0" ]; then
    PROGRAM="mapping0"
  elif [ "$HOSTNAME" = "mapping1" ]; then
    PROGRAM="mapping1"
  else
    echo "Choose a program [server, mapping0, mapping1]"
    read -r PROGRAM
  fi
fi
if [ "$PROGRAM" = "server" ]; then
  ./server/main.py
elif [ "$PROGRAM" = "server_recovery" ]; then
  ./server/recovery_console.py
elif [ "$PROGRAM" = "mapping0" ]; then
  brickrun -r "./mapping0/main.py"
elif [ "$PROGRAM" = "mapping1" ]; then
  brickrun -r "./mapping1/main.py"
else
  echo "Program not found"
fi
