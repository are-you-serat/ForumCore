import psycopg
from fastapi import HTTPException

def create_thread_table():
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS threads (
             threadID SERIAL PRIMARY KEY,
             thread_title TEXT NOT NULL,
             thread_text TEXT NOT NULL,
             user_id INT,
             FOREIGN KEY (user_id) REFERENCES users(user_id));''')

def insert_thread(thread_title, thread_text, thread_id):
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO threads (thread_title, thread_text, user_id) VALUES (%s, %s, %s)''', (thread_title, thread_text, thread_id))

def is_thread_exists(thread_id: int):
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT threadID FROM threads WHERE threadID = %s''', (thread_id,))
            result = cur.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Thread doesn't exists")