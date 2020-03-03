import sqlite3
class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'select * from items as i where i.name = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        if row:
            return {'id': row[0], 'name': row[1], 'price': row[2]}
        return None

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

    @classmethod
    def update_item_to_db(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = 'update items set price =? where name=?'
        cursor.execute(update_query, (item['price'], item['name'],))
        connection.commit()
        connection.close()