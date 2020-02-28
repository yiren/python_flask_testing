from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'joo'
api = Api(app)

items = []
jwt = JWT(app, authenticate, identity)
class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404


    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': f'Items with name {name} already exists.'}, 400
        parser = reqparse.RequestParser()
        parser.add_argument('price', type=float, required= True, help="Price cannot be blank.")
        data = parser.parse_args()
        new_item = {
            'name': name,
            'price': data['price']
        }
        items.append(new_item)
        return new_item, 201

    def delete(self, name):
        #global items
        return list(filter(lambda x: x['name'] != name, items))

    def put(self, name):
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
        return item

class ItemList(Resource):
    def get(self):
        return {'items': items}, 200

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__': # Only called when running 'app.py,' running not from imports
    app.run(debug=True, port=5001)