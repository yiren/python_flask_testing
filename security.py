from werkzeug.security import safe_str_cmp
from user import User
import sqlite3

users = [
    User(1, 'bob', 'asdf')
]

username_mapping = {u.name: u for u in users}

userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    #user = username_mapping.get(username, None)

    user = User.find_user_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):

    return User.find_user_by_id(payload['identity'])
