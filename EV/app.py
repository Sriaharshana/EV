from flask import Flask, render_template, request, jsonify
import sqlite3
import smtplib
from config import EMAIL_USER, EMAIL_PASS

app = Flask(__name__)

# Create Database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stations 
                 (id INTEGER PRIMARY KEY, name TEXT, address TEXT, available INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings 
                 (id INTEGER PRIMARY KEY, station_id INTEGER, user_email TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/stations')
def get_stations():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stations WHERE available = 1")
    stations = [{"id": row[0], "name": row[1], "address": row[2]} for row in c.fetchall()]
    conn.close()
    return jsonify({"stations": stations})

@app.route('/book/<int:station_id>', methods=['POST'])
def book_station(station_id):
    user_email = request.args.get("email", "user@example.com")
    
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE stations SET available = 0 WHERE id = ?", (station_id,))
    c.execute("INSERT INTO bookings (station_id, user_email) VALUES (?, ?)", (station_id, user_email))
    conn.commit()
    conn.close()

    send_email(user_email, "EV Charging Station Booking Confirmed", f"Your booking at station {station_id} is confirmed!")
    
    return jsonify({"message": "Booking successful! Confirmation sent to email."})

def send_email(to_email, subject, body):
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_USER, to_email, message)

if __name__ == '__main__':
    app.run(debug=True)
