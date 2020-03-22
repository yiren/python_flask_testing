from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from schema.user import UserSchema

user_schema = UserSchema()


# '_' implies private variable, and reuse within this file
# _user_parser = reqparse.RequestParser()
# _user_parser.add_argument('username', type=str, required=True, help='Username is required')
# _user_parser.add_argument('password', type=str, required=True, help='Password is required')


class UserRegister(Resource):
    @classmethod
    def post(self):
        try:
            json = request.get_json()
            user = user_schema.load(json)
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_user_by_username(user.username):
            return {'message': f'User {user.username} already exists.'}

        # user = UserModel(data['username'], data['password'])
        user.save_user_to_db()
        return {'message': f'User {user.username} is created'}, 201


class User(Resource):
    @classmethod
    def get(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user_schema.dump(user)

    @classmethod
    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message': 'User not exists'}, 404
        user.delete_user_in_db()
        return {'message': 'User was deleted'}


# manually implement authenticate() provided in flask-jwt
class UserLogin(Resource):
    @classmethod
    def post(self):
        try:
            json = request.get_json()
            user = user_schema.load(json)
        except ValidationError as err:
            return err.messages, 400

        user_db = UserModel.find_user_by_username(user.username)
        if user and safe_str_cmp(user_db.password, user.password):
            return {
                       # manually implement identity() provided in flask-jwt
                       'access_token': create_access_token(identity=user.id, fresh=True),
                       'refresh_token': create_refresh_token(user.id)
                   }, 200

        return {'message': 'Invalid credential.'}, 401


# implement refresh_token
class RefreshToken(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        return {
            'access_token': create_access_token(identity=user_id, fresh=False)
        }
