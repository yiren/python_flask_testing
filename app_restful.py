from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import ItemList, Item

app = Flask(__name__)
app.secret_key = 'joo'
#sqlalchemy package has its own tracker, disable the one implemented in the flask_sqlalchemy package
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


jwt = JWT(app, authenticate, identity)


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__': # Only called when running 'app.py,' running not from imports
    from orm import orm
    orm.init_app(app)
    app.run(debug=True, port=5001)