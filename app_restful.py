from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from orm import orm

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.store import StoreList, Store
from resources.item import ItemList, Item


app = Flask(__name__)
app.secret_key = 'joo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#sqlalchemy package has its own tracker, disable the one implemented in the flask_sqlalchemy package
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)

@app.before_first_request
def create_tables():
    orm.create_all()

jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')

api.add_resource(UserRegister, '/register')

if __name__ == '__main__': # Only called when running 'app.py,' running not from imports

    orm.init_app(app)
    app.run(debug=True, port=5001)