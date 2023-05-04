#!/usr/bin/env sh
# run custom tests
# start a MAPPING server
mkdir -r "$(pwd)/test/logs"
./server/main.py > "$(pwd)/test/logs/server_log.log" &
MAPPING_SERVER_PID="$!"
echo "Press enter to stop"
# shellcheck disable=SC2034
read -r UNUSED
# stop all running processes started by this script
kill -term "$MAPPING_SERVER_PID"
# remove test files
rm -r "$(pwd)/test/test_files/*"
