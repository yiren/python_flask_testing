from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="Price cannot be blank.")
    parser.add_argument('store_id', type=int, required=True, help="Store is required.")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {'item': item.json()}
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': f'Item already exists.'}, 400
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        # try:
        item.save_item_to_db()
        # except:
        #     return {'message': 'Error occurred when inserting a record'}, 500
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin is required'}, 401

        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_item_in_db()
            return {'message': f'{name} was deleted'}
        else:
            return {'message': f'{name} not exists'}

    def put(self, name):
        item = ItemModel.find_item_by_name(name)
        data = self.parser.parse_args()
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])
        item.save_item_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = ItemModel.get_items_from_db()
        if user_id:
            return {'items': [item.json() for item in items]}, 200
        return {
            'items': [item.name for item in items],
            'message': 'more data will be available when you login'
        }
