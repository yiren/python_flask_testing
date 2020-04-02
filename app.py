import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restful import Api
from marshmallow import ValidationError

from ma import ma
# from flask_jwt import JWT
from orm import orm
from resources.item import ItemList, Item
from resources.store import StoreList, Store
# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, RefreshToken

app = Flask(__name__)
load_dotenv('.env')
app.secret_key = 'joo'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///data.db')
# sqlalchemy package has its own tracker, disable the one implemented in the flask_sqlalchemy package
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = [
    'access',
    'refresh'
]

api = Api(app)

orm.init_app(app)
Migrate(app, orm)


@app.before_first_request
def create_tables():
    orm.create_all()


jwt = JWTManager(app)


@app.errorhandler(ValidationError)
def handle_marshmallow_error(err):
    return jsonify(err.messages), 400


# jwt = JWT(app, authenticate, identity)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:  # should avoid hard-code role, read from config or db
        return {'is_admin': True}
    return {'is_admin': False}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(RefreshToken, '/refresh')

# uWSGI would not run the code below
if __name__ == '__main__':  # Only called when running 'app_basic.py,' running not from imports

    ma.init_app(app)
    app.run(debug=True, port=5001)
