import psycopg

def create_comments_table():
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS comments (
                        commentID SERIAL PRIMARY KEY,
                        tredID INT,
                        comment TEXT NOT NULL,
                        user_id INT,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    );''')

def insert_comment(comment, user_id, tred_id):
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''INSERT INTO comments (comment, user_id, tredID) VALUES (%s, %s, %s)''', (comment, user_id, tred_id))


def get_messages_by_userid_db(username):
    with psycopg.connect(dbname='postgres', host='localhost', user='postgres', password='serat') as conn:
        with conn.cursor() as cur:
            cur.execute('''
                SELECT comments.comment
                FROM comments
                JOIN users ON comments.user_id = users.user_id
                WHERE users.username = %s;
            ''', (username,))
            result = cur.fetchall()
            return result