
# Bank of SQotLand (BOSQL) - A simple web application that demonstrates how not to handle user input and database queries.
# Author: Kieran Gordon <kjg2000@hw.ac.uk>
# Date: 2024-02-29
# Licensed under the GNU Affero General Public License v3.0. See LICENSE for details.

import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

conn = sqlite3.connect('bankofsql.db')
conn.executescript("PRAGMA foreign_keys = 1")
c = conn.cursor()
try:
    c.executescript('''CREATE TABLE user (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, password TEXT, email TEXT, dob TEXT, card_number TEXT, cvv TEXT, expiry_date TEXT, balance TEXT)''')
except:
    pass
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register_user():
    """Register a new user. I love Raw SQL, don't you? It's so safe and secure!

    Returns:
        render_template: Register page if no arguments are passed
        render_template: Login page if user is registered
    """
    if 'email' not in request.args or 'password' not in request.args or 'first_name' not in request.args or 'last_name' not in request.args or 'dob' not in request.args:
        return render_template('register.html')
    first_name = request.args['first_name']
    last_name = request.args['last_name']
    email = request.args['email']
    password = request.args['password']
    dob = request.args['dob']
    conn = sqlite3.connect('bankofsql.db')
    c = conn.cursor()
    # For anyone who's not familiar with SQL Injection, this is a prime example of how not to handle user input. Please don't do this.
    c.executescript("INSERT INTO user (first_name, last_name, email, password, dob, balance) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 0)".format(first_name, last_name, email, password, dob))
    conn.commit()
    conn.close()
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login_user():
    """Login as a user. Note that we are not using sessions, so this is not a secure way to handle logins.

    Returns:
        render_template: Login page if no arguments are passed
        render_template: Dashboard page if user is logged in
    """
    if 'email' not in request.args or 'password' not in request.args:
        return render_template('login.html')
    email = request.args['email']
    password = request.args['password']
    conn = sqlite3.connect('bankofsql.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE email = '{0}' AND password = '{1}'".format(email, password))
    user = c.fetchone()
    conn.close()
    if user is None:
        return render_template('login.html')
    return render_template('dashboard.html', user=user)

@app.route('/logout', methods=['GET'])
def logout_user():
    """Log out of the system. Of course since we are not using sessions, this is not really necessary.
    For all intensive purposes, anyone who's serious about making a website should just use sessions.
    But for the sake of this example, we will just redirect to the login page. Please, never do this in production.

    Returns:
        render_template: Login page
    """
    return render_template('index.html')

@app.route('/add_card', methods=['GET'])
def add_card():
    """Add a card to a user's account. This is definitely safe and secure, right? Right...?

    Returns:
        render_template: Dashboard page
    """
    user_id = request.args.get('user_id')
    card_number = request.args.get('card_number')
    expiry_date = request.args.get('expiry_date')
    cvv = request.args.get('cvv')
    conn = sqlite3.connect('bankofsql.db')
    c = conn.cursor()
    c.executescript("UPDATE user SET card_number = '{0}', expiry_date = '{1}', cvv = '{2}' WHERE id = {3}".format(card_number, expiry_date, cvv, user_id))
    conn.commit()
    user = c.execute("SELECT * FROM user WHERE id = {0}".format(user_id)).fetchone()
    conn.close()
    return render_template('dashboard.html', user=user)

@app.route('/deposit', methods=['GET'])
def deposit():
    """Deposit money into a user's account. Note that no money is actually being deposited, so rest assured that this is a safe and secure transaction.

    Returns:
        render_template: Dashboard page
    """
    amount = request.args['amount']
    conn = sqlite3.connect('bankofsql.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE id = {0}".format(request.args['user_id']))
    user = c.fetchone()
    c.executescript("UPDATE user SET balance = balance + {0} WHERE id = {1}".format(amount, request.args['user_id']))
    conn.close()
    return render_template('dashboard.html', user=user)

@app.route('/withdraw', methods=['GET'])
def withdraw():
    """Withdraw money from a user's account. Where does the money go? Who knows! It's a mystery!

    Returns:
        render_template: Dashboard page
    """
    amount = request.args['amount']
    conn = sqlite3.connect('bankofsql.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE id = {0}".format(request.args['user_id']))
    user = c.fetchone()
    c.executescript("UPDATE user SET balance = balance - {0} WHERE id = {1}".format(amount, request.args['user_id']))
    conn.close()
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    """Run the application. This is the main entry point for the application. It will start the server and listen for requests.
    Better yet, it runs in debug mode, so you can see all the errors in the console. What could go wrong?
    """
    app.run(debug=True)