import mariadb  # pip install mariadb

_db = None
_cursor = None


def connect(address, username, user_password, use_database):
    # connect to the database and initialize it
    global _db, _cursor
    _db = mariadb.connect(host=address, user=username, password=user_password, database=use_database)
    _cursor = _db.cursor()
    _db.autocommit = True


def disconnect():
    _db.close()


def execute(sql_statement):
    _cursor.execute(sql_statement)


def fetch(sql_statement):
    _cursor.execute(sql_statement)
    return _cursor.fetchall()


def does_table_exist(table_name):
    # check if lb table exists
    _cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'".format(
        table_name.replace('\'', '\'\'')))
    if _cursor.fetchone()[0] == 1:
        return True
    return False


if __name__ == '__main__':
    # example to test this script
    password = open('DBPassword.txt', 'r').readline().rstrip()
    connect('localhost', 'MAPPING_server', password, 'MAPPING')
    print(fetch('SHOW DATABASES'))
    disconnect()
