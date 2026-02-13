# Sports Tracker Application

A modern, clean web application for tracking users' favorite sports. Built with Flask and SQLite.

## Features

- **User Signup**: Create an account with username, password, and favorite sport
- **User Search**: Look up other users and discover their favorite sports
- **Modern UI**: Clean, responsive design with a professional look
- **SQLite Database**: Lightweight database with proper relationships

## Database Schema

### Tables

1. **users**
   - `id` (INTEGER, PRIMARY KEY)
   - `username` (TEXT, UNIQUE)
   - `password` (TEXT, hashed with SHA-256)
   - `created_at` (TIMESTAMP)

2. **sports**
   - `id` (INTEGER, PRIMARY KEY)
   - `username` (TEXT, UNIQUE, FOREIGN KEY)
   - `sport` (TEXT)
   - `created_at` (TIMESTAMP)

## Setup

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the database**:
   ```bash
   python db_setup.py
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the app**:
   Open your browser to `http://localhost:3000`

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

2. **Access the app**:
   Open your browser to `http://localhost:3000`

3. **Stop the application**:
   ```bash
   docker-compose down
   ```

## Usage

### Home Page
- Welcome screen with information about why sports are important
- Two buttons: "Sign Up" and "Search Users"

### Sign Up Page
- Username (minimum 3 characters)
- Password (minimum 6 characters)
- Favorite Sport (with suggestions)

### Search Users Page
- Enter a username to search
- Results display on the same page showing the user's favorite sport

## Security Features

- Password hashing using SHA-256
- Input validation on all forms
- Proper error handling

## Technology Stack

- **Backend**: Python 3.11, Flask 3.0
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (Modern design)
- **Deployment**: Docker, Docker Compose

## Project Structure

```
demo-app/
├── app.py              # Main Flask application
├── db_setup.py         # Database initialization script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── static/
│   └── style.css      # Modern CSS styling
└── templates/
    ├── index.html     # Home page
    ├── signup.html    # Signup page
    └── search.html    # Search page
```

## License

MIT License - Feel free to use this project for learning and development purposes.
