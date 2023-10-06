import sqlite3
conn=sqlite3.connect('sensor_data.db')
curs=conn.cursor()
print ("\nLast raw Data logged on database:\n")
for row in curs.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1"):
    print (str(row[0])+" ==> Temp = "+str(row[1])+"	Hum ="+str(row[2]))