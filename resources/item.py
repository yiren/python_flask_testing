from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="Price cannot be blank.")
    parser.add_argument('store_id', type=int, required=True, help="Store is required.")

    @jwt_required()
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

    def delete(self, name):
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
    def get(self):
        items = ItemModel.get_items_from_db()
        return {'items': [item.json() for item in items]}, 200
