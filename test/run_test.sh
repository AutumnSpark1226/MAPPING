#!/usr/bin/env sh
# run custom tests
# detect running mariadb server
MYSQL_RUNNING=$(pgrep mysql | wc -l)
if [ "$MYSQL_RUNNING" -eq 1 ]; then
  echo "Please stop the running mariadb server"
  exit 1
fi
echo "Please make sure that port 3306 ist properly firewalled. Press enter to continue"
# shellcheck disable=SC2034
read -r UNUSED
# setup a test database server
MYSQL_ROOT="$(pwd)/test/test_files/database"
if [ ! -d "${MYSQL_ROOT}" ]; then
  mkdir -p "${MYSQL_ROOT}"
  mysql_install_db "--datadir=${MYSQL_ROOT}" "--basedir=/usr/"
fi
mysqld "--datadir=${MYSQL_ROOT}" &
MYSQL_PID="$!"
# backup original database password
mv ./server/DBPassword.txt ./server/DBPassword.txt.backup
# create new random database password
cat /proc/sys/kernel/random/uuid > ./server/DBPassword.txt
echo "CREATE OR REPLACE DATABASE MAPPING" | mariadb -u root
echo "CREATE USER MAPPING_server@localhost IDENTIFIED BY '$(cat ./server/DBPassword.txt)'" | mariadb -u root
echo "GRANT ALL PRIVILEGES ON MAPPING.* TO MAPPING_server@localhost"  | mariadb -u root
echo "FLUSH PRIVILEGES" | mariadb -u root
# start a MAPPING server
./server/main.py &
MAPPING_SERVER_PID="$!"
echo "Press enter to stop"
read -r UNUSED
# stop all running processes started by this script
kill -term "$MAPPING_SERVER_PID"
kill -term "$MYSQL_PID"
# remove test files
mv ./server/DBPassword.txt.backup ./server/DBPassword.txt
rm -r "$(pwd)/test/test_files/*"
