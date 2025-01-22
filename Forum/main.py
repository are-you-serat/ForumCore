from fastapi import FastAPI, HTTPException
from authx import AuthX, AuthXConfig, RequestToken
from fastapi.params import Depends
from schemes import UserSchema, CommentSchema, ThreadSchema
from registration import insert_user, create_user_table, hash_password, verify_password, get_user
from comments import create_comments_table, insert_comment, get_messages_by_userid_db
from threads import create_thread_table, insert_thread, is_thread_exists
import jwt
import psycopg

app = FastAPI()
secret_key = 'SECRET_KEY'
algorithm = 'HS256'

config = AuthXConfig()
config.JWT_ALGORITHM = algorithm
config.JWT_SECRET_KEY = secret_key
auth = AuthX(config)
create_user_table()
create_comments_table()
create_thread_table()

admins = ['serat'] # Лист с админами форума

@app.post('/register')
def register(user: UserSchema):
    try:
        hashed_pass = hash_password(user.password)
        insert_user(user.username, hashed_pass)
        return {'success': 'User registered successfully'}
    except psycopg.errors.UniqueViolation:
        raise HTTPException(status_code=409, detail='Username already exists')


@app.post('/login')
def login(user: UserSchema):
    try:
        user_from_db = get_user(user.username)
        ver_pass = verify_password(user.password, user_from_db[2])
        if user_from_db[1] == user.username and ver_pass and user.username in admins: # Аутентификация для админов. Выдача админского JWT
            payload = {
                'role': 'admin',
                'username': user.username,
                'user_id': user_from_db[0]
            }
            token = auth.create_access_token(uid=user.username, data=payload)
            return {'access_token' : token}
        elif user_from_db[1] == user.username and ver_pass: # Аутентификация для обычных пользователей. Выдача обычного JWT токена
            payload = {
                'role': 'user',
                'username': user.username,
                'user_id': user_from_db[0]
            }
            token = auth.create_access_token(uid=user.username, data=payload)
            return {'access_token': token}
    except TypeError:
        ...
    raise HTTPException(status_code=401, detail='Invalid credentials')

@app.post('/post_comment/{thread_id}', dependencies=[Depends(auth.get_token_from_request), Depends(is_thread_exists)], summary='Post comment into tred')
def post_comment(thread_id: int, comment: CommentSchema, token: RequestToken = Depends()):
    verify_bool = auth.verify_token(token)
    decoded_token = jwt.decode(token.token, secret_key, algorithms=[algorithm])
    user_id = decoded_token['user_id']
    if verify_bool:
        insert_comment(comment.comment, user_id, thread_id)
        return {'success': 'Post added successfully'}
    else:
        raise HTTPException(status_code=401, detail='Invalid token')

@app.post('/create_thread', dependencies=[Depends(auth.get_token_from_request)], summary='Create a thread')
def create_thread(thread: ThreadSchema, token: RequestToken = Depends()):
    verify_bool = auth.verify_token(token)
    decoded_token = jwt.decode(token.token, secret_key, algorithms=[algorithm])
    user_id = decoded_token['user_id']
    if verify_bool:
        insert_thread(thread.thread_title, thread.thread_text, user_id)
        return {'success': 'Thread created successfully'}
    else:
        raise HTTPException(status_code=401, detail='Invalid token')



@app.get('/get_messages_by_userid/{username}', dependencies=[Depends(auth.get_token_from_request)], summary='Retrieve all user messages by ID. Only for admins')
def get_messages_by_userid(username: str, token: RequestToken = Depends()):
    try:
        decoded_token = jwt.decode(token.token, secret_key, algorithms=[algorithm])
        if decoded_token['role'] == 'user':
            raise HTTPException(status_code=403, detail='Access denied')
        elif decoded_token['role'] == 'admin':
            result = get_messages_by_userid_db(username)
            return {'result': result}
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(status_code=401, detail='Signature verification failed')