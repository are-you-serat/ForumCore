# ForumCore

This is a backend for a forum built using **FastAPI** — a modern, fast (high-performance) web framework for building APIs with Python.

## Key Features

- **Topic Management**: Users can create and manage discussion topics.
- **Comments**: Users can post comments under topics.
- **Authentication and Authorization**: User registration and login system implemented using JWT (JSON Web Tokens).
- **Password Hashing**: User passwords are securely hashed using **bcrypt** for enhanced security.

## Technologies

- **FastAPI** — the main framework for building the API.
- **Psycopg** — PostgreSQL database adapter for Python.
- **Pydantic** — for data validation and serialization.
- **authx** — for user authentication and authorization.
- **PyJWT** — for JWT token decode
- **PostgreSQL** — the database for storing information.
- **Bcrypt** — for secure password hashing.

## Installation
- Clone repo.
- ```pip install -r requirements.txt```
- Start dev server: ```fastapi dev main.py```
- Go to http://127.0.0.1:8000/docs for docs.
