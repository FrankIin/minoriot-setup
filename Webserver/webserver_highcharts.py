from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index_2.html')

@app.route('/data')
def get_data():
    conn = sqlite3.connect('sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp , temperature FROM sensor_data')
    data = cursor.fetchall()
    conn.close()
    
    formatted_data = [{'timestamp': row[0], 'temperature': row[1]} for row in data]
    
    return jsonify(formatted_data)

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=1025, debug=False)
