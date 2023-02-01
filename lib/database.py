import mariadb  # pip install mariadb

# TODO replace after updating mariadb
# _db: mariadb.connections.Connection
# _cursor: mariadb.connections.Connection.cursor
_db: mariadb.connection
_cursor: mariadb.connection.cursor

"""
not further explanation needed
"""


def connect(address: str, username: str, user_password: str, use_database: str):
    # connect to the database and initialize it
    global _db, _cursor
    _db = mariadb.connect(host=address, user=username, password=user_password, database=use_database, autocommit=True)
    _cursor = _db.cursor()


def disconnect():
    global _db, _cursor
    if not _db or not _cursor:
        raise Exception("database not connected")
    _db.close()


def execute(sql_statement: str):
    if not _db or not _cursor:
        raise Exception("database not connected")
    _cursor.execute(sql_statement)


def fetch(sql_statement: str):
    if not _db or not _cursor:
        raise Exception("database not connected")
    _cursor.execute(sql_statement)
    return _cursor.fetchall()


def does_table_exist(table_name: str):
    if not _db or not _cursor:
        raise Exception("database not connected")
    # check if table exists
    _cursor.execute(
        "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '" + table_name.replace('\'', '\'\''))
    if _cursor.fetchone()[0] == 1:
        return True
    return False
