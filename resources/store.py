from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required = True, help='name is required')
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return {'store': store}
        return {'message': 'Store not found.'}, 404

    def post(self, name):
        if StoreModel.find_store_by_name(name):
            return {'message': f'Store {name} already exists.'}, 400
        store = StoreModel(name)

        # try:
        store.save_store_to_db()
        # except:
        #     return {'message': 'Error occurred when inserting a record'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_store_in_db()
            return {'message': f'{name} was deleted'}
        else:
            return {'message': f'{name} not exists'}

    def put(self, name):
        store = StoreModel.find_store_by_name(name)
        data = self.parser.parse_args()
        if store:
            store = StoreModel(**data)
        else:
            store = StoreModel(name)
        store.save_store_to_db()
        return store.json()


class StoreList(Resource):
    def get(self):
        stores = StoreModel.get_stores_from_db()
        return {'stores': [store.json() for store in stores]}, 200
