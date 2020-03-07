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

        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_user_to_db()
        return {'message': f'User {user.username} is created'}, 201


class User(Resource):


    def get(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'nessage': 'User not found'}, 404
        return user.json()


    def delete(self, user_id):
        user = UserModel.find_user_by_id(user_id)
        if not user:
            return {'message': 'User not exists'}, 404
        user.delete_user_in_db()
        return {'message': 'User was deleted'}
