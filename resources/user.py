import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_user_by_username(data['username']):
            return {'message': f'User {data["username"]} already exists.'}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = 'insert into users values(null, ?, ?)'
        cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': f'User {data["username"]} is created'}, 201