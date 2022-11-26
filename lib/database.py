import mariadb  # pip install mariadb

_db = None
_cursor = None


def connect(address, username, user_password, use_database):
    # connect to the database and initialize it
    global _db, _cursor
    _db = mariadb.connect(host=address, user=username, password=user_password, database=use_database, autocommit=True)
    _cursor = _db.cursor()


def disconnect():
    global _db, _cursor
    if not _db or not _cursor:
        raise Exception("database not connected")
    _db.close()
    _db = None
    _cursor = None


def execute(sql_statement):
    if not _db or not _cursor:
        raise Exception("database not connected")
    _cursor.execute(sql_statement)


def fetch(sql_statement):
    if not _db or not _cursor:
        raise Exception("database not connected")
    _cursor.execute(sql_statement)
    return _cursor.fetchall()


def does_table_exist(table_name):
    if not _db or not _cursor:
        raise Exception("database not connected")
    # check if table exists
    _cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'".format(
        table_name.replace('\'', '\'\'')))
    if _cursor.fetchone()[0] == 1:
        return True
    return False
