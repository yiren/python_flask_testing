import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items =[]

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="Price cannot be blank.")
    @jwt_required()
    def get(self, name):

        item = self.find_item_by_name(name)
        if item:
            return {'item':item}
        return {'message':'Item not found.'}, 404


    def post(self, name):
        if self.find_item_by_name(name):
            return {'message': f'Item already exists.'}, 400
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        try:
            data = self.insert_item_into_db(item)
            return data
        except:
            return {'message':'Error occured when inserting a record'}, 500


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = 'delete from items where name=?'
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()
        return {'message': 'The item was deleted.'}

    def put(self, name):
        item = self.find_item_by_name(name)
        data = self.parser.parse_args()
        updated_item = {
            'name': name,
            'price': data['price']
        }
        try:
            if item:
                self.update_item_to_db(updated_item)
                return self.find_item_by_name(name)
            else:
                self.insert_item_into_db(updated_item)
        except:
            return {'message': 'An error occurred when updating the item'}, 500

class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'select * from items'
        result = cursor.execute(query)
        items=[]
        for row in result:
            items.append({
                'id':row[0],
                'name':row[1],
                'price':row[2],
            })
        connection.close()
        return {'items': items}, 200