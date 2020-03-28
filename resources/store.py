from flask_restful import Resource

from models.store import StoreModel
from schema.store import StoreSchema

store_schema = StoreSchema()
list_store_schema = StoreSchema(many=True)


class Store(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument('name', required = True, help='name is required')
    def get(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            return {'store': store_schema.dump(store)}
        return {'message': 'Store not found.'}, 404

    def post(self, name):
        if StoreModel.find_store_by_name(name):
            return {'message': f'Store {name} already exists.'}, 400
        store = StoreModel(name=name)

        try:
            store.save_store_to_db()
        except:
            return {'message': 'Error occurred when inserting a record'}, 500
        return store_schema.dump(store), 201

    def delete(self, name):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_store_in_db()
            return {'message': f'{name} was deleted'}
        else:
            return {'message': f'{name} not exists'}

    # def put(self, name):
    #     store = StoreModel.find_store_by_name(name)
    #     data = request.get_json()
    #     if store:
    #         store.name = data['name']
    #     else:
    #         store = StoreModel(name = name)
    #     store.save_store_to_db()
    #     return store_schema.dump(store)


class StoreList(Resource):
    def get(self):
        # stores = StoreModel.get_stores_from_db()
        # return {'stores': [store.json() for store in stores]}, 200
        return {'stores': list_store_schema(StoreModel.get_stores_from_db())}
