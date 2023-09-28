import sqlite3

# 1. Connect to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('sensor_data.db')

# 2. Create a cursor object to interact with the database
cursor = conn.cursor()

# 3. Execute an SQL query to fetch data (replace 'your_table' and 'your_column' with your actual table and column names)
cursor.execute('SELECT * FROM sensor_data')

# 4. Fetch and print the data
for row in cursor.fetchall():
    print(row)

# 5. Close the cursor and the database connection when done
cursor.close()
conn.close()