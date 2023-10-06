from flask import Flask, render_template, request
app = Flask(__name__)
import sqlite3
# Retrieve data from database
def getData():
	conn=sqlite3.connect('sensor_data.db')
	curs=conn.cursor()
	for row in curs.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[5])
		temp = row[2]
		hum = row[3]
		pres = row[4]
	conn.close()
	return time, temp, hum, pres
# main route 
@app.route("/")
def index():	
	time, temp, hum, pres = getData()
	templateData = {
		'time': time,
		'temp': temp,
		'hum': hum,
		'pres': pres
	}
	return render_template('index_2.html', **templateData)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=1025, debug=False)