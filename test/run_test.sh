#!/usr/bin/env zsh
# run custom tests
# (who needs a testing database anyway)
rm "$(pwd)/test/logs/*"  # clear old logs
# start a MAPPING server
mkdir -p "$(pwd)/test/logs"
./server/main.py > "$(pwd)/test/logs/server_log.log" &
MAPPING_SERVER_PID="$!"
sleep 3
./venv/bin/python3 ./mapping0/main.py > "$(pwd)/test/logs/mapping0_log.log" &
MAPPING_MAPPING0_PID="$!"
./venv/bin/python3 ./mapping1/main.py > "$(pwd)/test/logs/mapping1_log.log" &
MAPPING_MAPPING1_PID="$!"
echo "Press enter to stop"
# shellcheck disable=SC2034
read -r UNUSED
# stop all running processes started by this script
kill -term "$MAPPING_SERVER_PID"
kill -term "$MAPPING_MAPPING0_PID"
kill -term "$MAPPING_MAPPING1_PID"
