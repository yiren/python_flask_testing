import sqlite3
from flask_restful import Resource, reqparse

class User:
    def __init__(self, _id, name, password):
        self.id = _id
        self.name = name
        self.password = password

    @classmethod
    def find_user_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'select * from users as u where u.username = ?'
        row = cursor.execute(query, (username,))
        result = row.fetchone()
        if result:
            user = cls(*result)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_user_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'select * from users as u where u.id = ?'
        row = cursor.execute(query, (_id,))
        result = row.fetchone()
        if result:
            user = cls(*result)
        else:
            user = None
        connection.close()
        return user

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')

    def post(self):
        data = UserRegister.parser.parse_args()
        if User.find_user_by_username(data['username']):
            return {'message': f'User {data["username"]} already exists.'}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = 'insert into users values(null, ?, ?)'
        cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': f'User {data["username"]} is created'}, 201