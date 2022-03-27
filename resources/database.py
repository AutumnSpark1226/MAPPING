import mysql.connector  # pip install mysql-connector-python

db = None
cursor = None


def connect(host, user, password, database):
    # connect to the database and initialize it
    try:
        global db, cursor
        db = mysql.connector.connect(host=host, user=user, password=password, database=database)
        cursor = db.cursor()
    except mysql.connector.Error as error:
        raise Exception('Can\'t connect to database: ' + str(error))


def disconnect():
    db.close()


def execute(sql_statement):
    cursor.execute(sql_statement)


def fetch(sql_statement):
    cursor.execute(sql_statement)
    return cursor.fetchall()


def does_table_exist(table_name):
    # check if a table exists
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'".format(
        table_name.replace('\'', '\'\'')))
    if cursor.fetchone()[0] == 1:
        return True
    return False


if __name__ == '__main__':
    # example to test this script
    connect('localhost', 'user', 'user', 'TEST')
    disconnect()
