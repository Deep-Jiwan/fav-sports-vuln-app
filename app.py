from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

DATABASE = 'sports_app.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        sport = request.form.get('sport', '').strip()
        
        # Validation
        if not username or not password or not sport:
            flash('All fields are required', 'error')
            return render_template('signup.html')
        
        if len(username) < 3:
            flash('Username must be at least 3 characters', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('signup.html')
        
        try:
            conn = get_db_connection()
            
            # Check if username already exists
            existing_user = conn.execute(
                'SELECT username FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            
            if existing_user:
                flash('Username already exists', 'error')
                conn.close()
                return render_template('signup.html')
            
            # Hash password
            hashed_password = hash_password(password)
            
            # Insert user
            conn.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed_password)
            )
            
            # Insert sport preference
            conn.execute(
                'INSERT INTO sports (username, sport) VALUES (?, ?)',
                (username, sport)
            )
            
            conn.commit()
            conn.close()
            
            flash('Signup successful!', 'success')
            return redirect(url_for('search'))
            
        except sqlite3.Error as e:
            flash(f'Database error: {str(e)}', 'error')
            return render_template('signup.html')
    
    return render_template('signup.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    from flask import request
    # get_db_connection is assumed to be defined elsewhere
    # ... rest of the function
    pass

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Check if database exists
    if not os.path.exists(DATABASE):
        print("Database not found. Please run db_setup.py first.")
        exit(1)
    
    app.run(host='0.0.0.0', port=3000, debug=False)
