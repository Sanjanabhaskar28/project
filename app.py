from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# MySQL connection setup
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sanjana@28',
    database='airticket',
)
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book')
def book():
    return render_template('book.html')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    name = request.form['name']
    email = request.form['email']
    origin = request.form['origin']
    destination = request.form['destination']
    flight_date = request.form['flight_date']

    cursor.execute("INSERT INTO bookings (name, email, origin, destination, flight_date) VALUES (%s, %s, %s, %s, %s)",
                   (name, email, origin, destination, flight_date))
    conn.commit()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/bookings')
def view_bookings():
    cursor.execute("SELECT * FROM bookings")
    data = cursor.fetchall()
    return render_template('view_bookings.html', bookings=data)

if __name__ == '__main__':
    app.run(debug=True)


