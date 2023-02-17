import mariadb
import sys

# Connect to the database
try:
    conn = mariadb.connect(
        user="myuser",
        password="mypassword",
        host="localhost",
        port=3306,
        database="mydatabase"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    sys.exit(1)

# Execute a query to retrieve the coordinates
cur = conn.cursor()
cur.execute("SELECT x_coord, y_coord FROM mytable")
rows = cur.fetchall()

# Compute the mean of the x-coordinates and y-coordinates
x_mean = sum(row[0] for row in rows) / len(rows)
y_mean = sum(row[1] for row in rows) / len(rows)

# Compute the standard deviation of the x-coordinates and y-coordinates
x_stdev = (sum((row[0] - x_mean)**2 for row in rows) / len(rows))**0.5
y_stdev = (sum((row[1] - y_mean)**2 for row in rows) / len(rows))**0.5

# Find the coordinates that are more than 3 standard deviations away from the mean
outliers = []
for row in rows:
    if abs(row[0] - x_mean) > 3 * x_stdev or abs(row[1] - y_mean) > 3 * y_stdev:
        outliers.append(row)

# Print the outliers
print("Outliers:")
for row in outliers:
    print(row)

# Close the database connection
conn.close()
