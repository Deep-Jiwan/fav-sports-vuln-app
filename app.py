from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, render_template_string
import sqlite3
import hashlib
import os
import pickle
import base64

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'sports_tracker_2024_secret')

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
    """Search user page"""
    result = None
    search_username = ''
    
    if request.method == 'POST':
        search_username = request.form.get('username', '').strip()
        
        if search_username:
            conn = get_db_connection()
            cursor = conn.execute("SELECT username, sport FROM sports WHERE username = ?", (search_username,))
            user_data = cursor.fetchall()
            
            conn.close()
            
            if user_data:
                results_list = []
                for row in user_data:
                    results_list.append({
                        'username': row['username'] if 'username' in row.keys() else row[0],
                        'sport': row['sport'] if 'sport' in row.keys() else row[1]
                    })
                
                result = {
                    'found': True,
                    'data': results_list
                }
            else:
                result = {
                    'found': False,
                    'username': search_username
                }
    
    return render_template('search.html', result=result, search_username=search_username)

@app.route('/preview_message', methods=['GET', 'POST'])
def preview_message():
    """Preview custom welcome message for your profile"""
    output = None
    if request.method == 'POST':
        template = request.form.get('message', '')
        if template:
            # Render user's custom message
            output = render_template_string(template)
    return render_template('preview_message.html', output=output)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    """View user profile and sports preferences"""
    conn = get_db_connection()
    user = conn.execute(
        'SELECT users.username, sports.sport FROM users LEFT JOIN sports ON users.username = sports.username WHERE users.rowid = ?',
        (user_id,)
    ).fetchone()
    conn.close()
    
    if user:
        return render_template('profile.html', user=user, user_id=user_id)
    else:
        return "User not found", 404

@app.route('/import_preferences', methods=['GET', 'POST'])
def import_preferences():
    """Import saved user preferences from backup"""
    result = None
    error = None
    if request.method == 'POST':
        data = request.form.get('backup_data', '')
        if data:
            try:
                # Restore user preferences from backup
                decoded = base64.b64decode(data)
                # Use json.loads instead of pickle.loads for safe deserialization
                import json
                obj = json.loads(decoded.decode('utf-8'))
                result = str(obj)
            except Exception as e:
                error = str(e)
    return render_template('import_preferences.html', result=result, error=error)

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
