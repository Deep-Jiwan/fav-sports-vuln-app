import sqlite3
import os

DATABASE = 'sports_app.db'

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
    conn.close()
    
    print("Database setup completed successfully!")
    print("\nTables created:")
    print("  - users (id, username, password, created_at)")
    print("  - sports (id, username, sport, created_at)")

if __name__ == '__main__':
    setup_database()
