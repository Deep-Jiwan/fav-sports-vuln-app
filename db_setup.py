import sqlite3
import os
import hashlib

DATABASE = 'sports_app.db'

def hash_password(password):
    """Hash password using SHA-256"""
    import bcrypt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()

def populate_sample_data(conn):
    """Add sample users and their sports preferences"""
    cursor = conn.cursor()
    
    # Sample data
    users = [
        ('alice_johnson', 'password123', 'Basketball'),
        ('bob_smith', 'securepass', 'Soccer'),
        ('carol_davis', 'mypass456', 'Tennis'),
        ('david_brown', 'pass1234', 'Swimming'),
        ('emma_wilson', 'qwerty789', 'Running'),
        ('frank_miller', 'abc12345', 'Cycling'),
        ('grace_lee', 'letmein99', 'Volleyball'),
        ('henry_clark', 'password1', 'Baseball'),
        ('iris_martinez', 'welcome2024', 'Badminton'),
        ('jack_anderson', 'pass9876', 'Golf'),
    ]
    
    print("\nAdding sample users...")
    for username, password, sport in users:
        hashed_password = hash_password(password)
        
        # Insert user
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (?, ?)',
            (username, hashed_password)
        )
        
        # Insert sport preference
        cursor.execute(
            'INSERT INTO sports (username, sport) VALUES (?, ?)',
            (username, sport)
        )
        
        print(f"  ✓ Added user: {username} (sport: {sport})")
    
    conn.commit()
    print(f"\nSuccessfully added {len(users)} sample users!")

def setup_database():
    """Initialize the database with required tables"""
    
    # Remove existing database if it exists
    if os.path.exists(DATABASE):
        print(f"Removing existing database: {DATABASE}")
        if os.path.isdir(DATABASE):
            import shutil
            shutil.rmtree(DATABASE)
        else:
            os.remove(DATABASE)
    
    print(f"Creating new database: {DATABASE}")
    
    # Create connection
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create sports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            sport TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_sports_username ON sports(username)')
    
    conn.commit()
    
    print("Database setup completed successfully!")
    print("\nTables created:")
    print("  - users (id, username, password, created_at)")
    print("  - sports (id, username, sport, created_at)")
    
    # Populate with sample data
    populate_sample_data(conn)
    
    conn.close()

if __name__ == '__main__':
    setup_database()
