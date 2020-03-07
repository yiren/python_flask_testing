from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.user import UserModel

# '_' implies private variable, and reuse within this file
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', type=str, required=True, help='Username is required')
_user_parser.add_argument('password', type=str, required=True, help='Password is required')


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_user_by_username(data['username']):
            return {'message': f'User {data["username"]} already exists.'}

        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_user_to_db()
        return {'message': f'User {user.username} is created'}, 201


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message': 'User not exists'}, 404
        user.delete_user_in_db()
        return {'message': 'User was deleted'}


# manually implement authenticate() provided in flask-jwt
class UserLogin(Resource):

    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_user_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            return {
                       # manually implement identity() provided in flask-jwt
                       'access_token': create_access_token(identity=user.id, fresh=True),
                       'refresh_token': create_refresh_token(user.id)
                   }, 200

        return {'message': 'Invalid credential.'}, 401
