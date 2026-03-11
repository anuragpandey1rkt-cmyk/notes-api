# Notes Management API

A REST API built with Flask that allows authenticated users to create and manage personal notes, with role-based access control.

## Tech Stack
- Python + Flask
- SQLite (via SQLAlchemy)
- JWT Authentication
- Bcrypt for password hashing

## Setup Instructions

1. Clone the repository
   git clone <your-repo-url>
   cd notes-api

2. Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install flask flask-sqlalchemy flask-jwt-extended bcrypt python-dotenv

4. Run the application
   python3 app.py

Server runs at http://127.0.0.1:5000

## API Endpoints

### Auth
- POST /register - Register a new user
- POST /login - Login and get token

### Notes (require Authorization header)
- POST /notes - Create a note
- GET /notes - Get your notes (admin gets all)
- PUT /notes/<id> - Update a note
- DELETE /notes/<id> - Delete a note

## Example Requests

### Register
POST /register
{
    "username": "anurag",
    "password": "test123",
    "role": "user"
}

### Login
POST /login
{
    "username": "anurag",
    "password": "test123"
}

### Create Note (add Bearer token in Authorization header)
POST /notes
{
    "title": "My note",
    "content": "Note content"
}

## Roles
- user: can only manage their own notes
- admin: can view and delete all notes