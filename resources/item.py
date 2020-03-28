from flask import request
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_refresh_token_required
from flask_restful import Resource
from marshmallow import ValidationError

from models.item import ItemModel
from schema.item import ItemSchema

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('price', type=float, required=True, help="Price cannot be blank.")
    # parser.add_argument('store_id', type=int, required=True, help="Store is required.")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {'item': item_schema.dump(item)}
        return {'message': 'Item not found.'}, 404

    @jwt_refresh_token_required
    def post(self, name):
        if ItemModel.find_item_by_name(name):
            return {'message': f'Item already exists.'}, 400
        item_json = request.get_json()
        item_json['name'] = name

        try:
            item = item_schema.load(item_json)
        except ValidationError as err:
            return err.messages, 400

        # item = ItemModel(name, **data)

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
        item_json = request.get_json()
        if item:
            item.price = item_json['price']
        else:
            item_json['name'] = name
            try:
                item = item_schema.load(item_json)
            except ValidationError as err:
                return err.messages, 400

        item.save_item_to_db()

        return item_schema.dump(item)


class ItemList(Resource):
    # @jwt_optional
    def get(self):
        return item_list_schema.dump(ItemModel.get_items_from_db())
        # user_id = get_jwt_identity()
        # items = ItemModel.get_items_from_db()
        # if user_id:
        #     return {'items': [item.json() for item in items]}, 200
        # return {
        #     'items': [item.name for item in items],
        #     'message': 'more data will be available when you login'
        # }
