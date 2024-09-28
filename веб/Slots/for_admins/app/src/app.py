import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(72)


# Database setup
def init_db():
    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            balance INTEGER DEFAULT 1000
        )
    ''')
    conn.commit()
    conn.close()


# Call this once to initialize the database
init_db()


# Function to get user balance
def get_balance(username):
    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username = ?", (username,))
    balance = c.fetchone()[0]
    conn.close()
    return balance


# Update balance
def update_balance(username, amount):
    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, username))
    conn.commit()
    conn.close()


# Routes
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect('casino.db')
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            conn.close()
            flash('Signup successful! Please login.')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            error = 'Username already exists!'
            return render_template('signup.html', error=error)

    return render_template('signup.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('casino.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    if user and check_password_hash(user[0], password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        error = 'Invalid credentials'
        return render_template('index.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('index'))

    balance = get_balance(session['username'])
    return render_template('dashboard.html', balance=balance)


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/spin', methods=['POST'])
def spin():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    number1 = data.get('number1')
    number2 = data.get('number2')
    number3 = data.get('number3')
    request_hash = data.get('hash')

    # Validate that the hash is correct
    if not validate_hash(number1, number2, number3, request_hash):
        return jsonify({"error": "Invalid request"}), 400

    current_balance = get_balance(session['username'])

    # Check if the user has enough balance to spin
    if current_balance < 100:
        return jsonify({
            "error": "Insufficient funds. You need at least $100 to spin.",
            "new_balance": current_balance
        }), 400

    # Check if user won
    if number1 == number2 == number3:
        winnings = 100
        update_balance(session['username'], winnings)
        return jsonify({
            "message": "You won!",
            "winnings": winnings,
            "new_balance": get_balance(session['username'])
        })
    else:
        loss = -100  # Deduct 100$ for loss
        update_balance(session['username'], loss)
        return jsonify({
            "message": "You lost",
            "loss": loss,
            "new_balance": get_balance(session['username'])
        })


@app.route('/shop', methods=['GET', 'POST'])
def shop():
    if 'username' not in session:
        return redirect(url_for('index'))

    current_balance = get_balance(session['username'])

    if request.method == 'POST':
        if current_balance >= 10000:
            update_balance(session['username'], -10000)
            return render_template('shop.html', success=True, message=os.getenv("FLAG", "flag{}"), balance=get_balance(session['username']))
        else:
            return render_template('shop.html', success=False, message="Not enough funds to buy the Flag.",
                                   balance=current_balance)

    return render_template('shop.html', balance=current_balance)

@app.errorhandler(500)
def handle_500_error(e):
    # Redirect the user to the same page (refresh)
    response = redirect(request.path)  # Redirect to the same URL

    # Clear all cookies (iterate over all the cookies in the request)
    for cookie in request.cookies:
        response.delete_cookie(cookie)

    return response

# Helper functions
def generate_random_number():
    import random
    return random.randint(0, 9)


def validate_hash(num1, num2, num3, request_hash):
    combined_string = f"{num1}{num2}{num3}"
    sha1_hash = hashlib.sha1(combined_string.encode()).hexdigest()
    double_md5 = hashlib.md5(hashlib.md5(sha1_hash.encode()).hexdigest().encode()).hexdigest()
    return request_hash == double_md5


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)