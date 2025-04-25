<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Air Ticket Booking</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Welcome to Air Ticket Booking</h1>
        <p>Book your flight easily and quickly!</p>
        <div style="text-align:center;">
            <a href="{{ url_for('book') }}">
                <button>Book a Flight</button>
            </a>
        </div>
    </div>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Book Flight</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h2>Flight Booking Form</h2>
        <form method="POST">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="number" name="flight_id" placeholder="Flight ID" required>
            <input type="text" name="seat_number" placeholder="Seat Number" required>
            <button type="submit">Book Now</button>
        </form>
    </div>
</body>
</html>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Booking Confirmed</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h2>Your booking was successful! 🎉</h2>
        <p>Thank you for booking with us.</p>
        <a href="{{ url_for('home') }}"><button>Back to Home</button></a>
    </div>
</body>
</html>
body {
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(to right, #a8edea, #fed6e3);
    margin: 0;
    padding: 0;
    color: #333;
}

.container {
    width: 80%;
    margin: 40px auto;
    background: #ffffffcc;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
}

h1, h2 {
    text-align: center;
    color: #5f27cd;
}

form {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

input, select {
    padding: 10px;
    font-size: 16px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

button {
    padding: 12px;
    background-color: #10ac84;
    color: white;
    font-size: 16px;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.3s ease;
}

button:hover {
    background-color: #0e9072;
}
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


-- ER Model for Air Ticket Booking System

-- Drop Database if it exists to avoid conflicts
DROP DATABASE IF EXISTS airticket;
CREATE DATABASE airticket;
USE airticket;

-- Users Table
CREATE TABLE Users (
    User_ID INT PRIMARY KEY,
    Full_Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Phone_Number VARCHAR(20),
    Password VARCHAR(255),
    User_Type ENUM('Passenger', 'Admin', 'Staff')
);

-- Airports Table
CREATE TABLE Airports (
    Airport_ID INT PRIMARY KEY,
    Airport_Name VARCHAR(255),
    City VARCHAR(100),
    Country VARCHAR(100)
);

-- Flights Table
CREATE TABLE Flights (
    Flight_ID INT PRIMARY KEY,
    Airline_Name VARCHAR(255),
    Departure_Airport INT,
    Arrival_Airport INT,
    Departure_Time DATETIME,
    Arrival_Time DATETIME,
    Total_Seats INT,
    Available_Seats INT,
    FOREIGN KEY (Departure_Airport) REFERENCES Airports(Airport_ID) ON DELETE CASCADE,
    FOREIGN KEY (Arrival_Airport) REFERENCES Airports(Airport_ID) ON DELETE CASCADE
);

-- Bookings Table
CREATE TABLE Bookings (
    Booking_ID INT PRIMARY KEY,
    User_ID INT,
    Flight_ID INT,
    Booking_Date DATETIME,
    Seat_Number VARCHAR(10),
    Booking_Status ENUM('Confirmed', 'Canceled', 'Pending'),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Flight_ID) REFERENCES Flights(Flight_ID) ON DELETE CASCADE
);

-- Payments Table
CREATE TABLE Payments (
    Payment_ID INT PRIMARY KEY,
    Booking_ID INT,
    Payment_Method ENUM('Credit Card', 'PayPal', 'Other'),
    Transaction_Status ENUM('Completed', 'Pending', 'Failed'),
    Amount DECIMAL(10,2),
    FOREIGN KEY (Booking_ID) REFERENCES Bookings(Booking_ID) ON DELETE CASCADE
);

-- Pricing Table
CREATE TABLE Pricing (
    Price_ID INT PRIMARY KEY,
    Flight_ID INT,
    Base_Fare DECIMAL(10,2),
    Taxes DECIMAL(10,2),
    Final_Price DECIMAL(10,2),
    FOREIGN KEY (Flight_ID) REFERENCES Flights(Flight_ID) ON DELETE CASCADE
);

-- Loyalty Program Table
CREATE TABLE Loyalty_Program (
    Loyalty_ID INT PRIMARY KEY,
    User_ID INT UNIQUE,
    Total_Points INT,
    Membership_Level ENUM('Silver', 'Gold', 'Platinum'),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
);
