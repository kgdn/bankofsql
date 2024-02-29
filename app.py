from flask import Flask, render_template, request
import sqlite3

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
    if 'email' not in request.args or 'password' not in request.args or 'first_name' not in request.args or 'last_name' not in request.args or 'dob' not in request.args:
        return render_template('register.html')
    first_name = request.args['first_name']
    last_name = request.args['last_name']
    email = request.args['email']
    password = request.args['password']
    dob = request.args['dob']
    conn = sqlite3.connect('bankofsql.db')
    c = conn.cursor()
    c.executescript("INSERT INTO user (first_name, last_name, email, password, dob, balance) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', 0)".format(first_name, last_name, email, password, dob))
    conn.commit()
    conn.close()
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login_user():
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
    return render_template('index.html')

@app.route('/add_card', methods=['GET'])
def add_card():
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
    amount = request.args['amount']
    conn = sqlite3.connect('bankofsql.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE id = {0}".format(request.args['user_id']))
    user = c.fetchone()
    c.executescript("UPDATE user SET balance = balance - {0} WHERE id = {1}".format(amount, request.args['user_id']))
    conn.close()
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)