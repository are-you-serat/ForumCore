import psycopg
from passlib.hash import bcrypt

def create_user_table():
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)''')

def insert_user(username, password):
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO users (username, password) VALUES (%s, %s)''', (username, password))

def hash_password(password):
    return bcrypt.hash(password)

def verify_password(query, password):
    return bcrypt.verify(query, password)

def get_user(username):
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT user_id, username, password FROM users WHERE username = %s''', (username,))
            user = cur.fetchone()
    return user