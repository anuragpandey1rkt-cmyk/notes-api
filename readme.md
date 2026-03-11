# Notes Management API

A REST API built with Flask that allows authenticated users to create and manage personal notes, with role-based access control, pagination, search, and Docker support.

## Tech Stack
- Python + Flask
- SQLite (via SQLAlchemy)
- JWT Authentication (Access + Refresh tokens)
- Bcrypt for password hashing
- Swagger UI for API documentation
- Docker

## Setup Instructions

### Option 1 - Run locally

1. Clone the repository
   git clone <your-repo-url>
   cd notes-api

2. Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies
   pip install flask flask-sqlalchemy flask-jwt-extended bcrypt python-dotenv flask-swagger-ui

4. Run the application
   python3 app.py

Server runs at http://127.0.0.1:5000

### Option 2 - Run with Docker

1. Build the image
   docker build -t notes-api .

2. Run the container
   docker run -p 5001:5000 notes-api

Server runs at http://127.0.0.1:5001

## API Documentation
Once the server is running, visit:
http://127.0.0.1:5000/docs

## API Endpoints

### Auth
- POST /register - Register a new user
- POST /login - Login and get access + refresh tokens
- POST /refresh - Get new access token using refresh token

### Notes (require Authorization: Bearer <token> header)
- POST /notes - Create a note
- GET /notes - Get your notes (admin gets all)
- GET /notes?page=1&per_page=5 - Paginated notes
- GET /notes?search=keyword - Search notes by title
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
Response:
{
    "access_token": "eyJ...",
    "refresh_token": "eyJ..."
}

### Create Note
POST /notes
Headers: Authorization: Bearer <access_token>
{
    "title": "My note",
    "content": "Note content"
}

### Refresh Token
POST /refresh
Headers: Authorization: Bearer <refresh_token>

### Search & Pagination
GET /notes?search=my&page=1&per_page=5
Headers: Authorization: Bearer <access_token>

## Roles
- user: can only manage their own notes
- admin: can view and delete all notes