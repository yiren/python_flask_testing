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

    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'select * from items as i where i.name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            return {'id':row[0], 'name': row[1], 'price': row[2]}
        return None
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

    @classmethod
    def insert_item_into_db(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = 'insert into items values (null, ?, ?)'
        cursor.execute(insert_query, (item['name'], item['price']))
        item_id = cursor.lastrowid
        last_query = f'select * from items as i where i.id = ?'
        result = cursor.execute(last_query, (item_id,))
        new_item_in_db = result.fetchone()
        connection.commit()
        connection.close()
        return new_item_in_db
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
    @classmethod
    def update_item_to_db(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = 'update items set price =? where name=?'
        cursor.execute(update_query, (item['price'], item['name'],))
        connection.commit()
        connection.close()
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