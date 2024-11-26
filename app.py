from flask import Flask, request, g, render_template, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
import sqlite3
from functools import wraps

 

load_dotenv()
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_key_if_not_set')  # Replace with default if not set

DATABASE = 'instance/alameda-county-voters.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == os.environ.get('FLASK_USERNAME') and password == os.environ.get('FLASK_PASSWORD'):
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    print(os.environ.get('FLASK_USERNAME'))
    return render_template('search.html')


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        name_first = request.form.get('name_first', '').strip()
        name_last = request.form.get('name_last', '').strip()
        phone_number = request.form.get('phone_number', '').strip()
        city = request.form.get('city', '').strip()
        address = request.form.get('address', '').strip().lower() 

        db = get_db()
        
        # Build the query based on provided input
        query = "SELECT * FROM acvoters WHERE 1=1"
        params = []
        
        if name_first:
            query += " AND LOWER(name_first) = LOWER(?)"
            params.append(name_first)
        if name_last:
            query += " AND LOWER(name_last) = LOWER(?)"
            params.append(name_last)
        if phone_number:
            query += " AND (phone_1 = ? OR phone_2 = ?)"
            params.extend([phone_number, phone_number])
        if city:
            query += " AND LOWER(city) = LOWER(?)"
            params.append(city)
        if address:
            # Use Mail Street for address search
            query += " AND LOWER(mail_street) LIKE ?"
            print("address: " + address)
            params.append(f"%{address}%")



        cur = db.execute(query, params)
        results = cur.fetchall()
        return render_template('results.html', results=results)
    
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003)