from orm import orm
class ItemModel(orm.Model):
    __tablename__ = 'items'
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(80))
    price = orm.Column(orm.Float(precision=2))


    store = orm.relationship('StoreModel')
    store_id = orm.Column(orm.Integer, orm.ForeignKey('stores.id'))

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
        }

    @classmethod # notice that this cannot be changed to class function/method but should be @classmethod
    def find_item_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_item_to_db(self):
        orm.session.add(self)
        orm.session.commit()

    def delete_item_in_db(self):
        orm.session.delete(self)
        orm.session.commit()

    @classmethod
    def get_items_from_db(cls):
        return cls.query.all()
    # def update_item_to_db(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     update_query = 'update items set price =? where name=?'
    #     cursor.execute(update_query, (self.price, self.name,))
    #     connection.commit()
    #     connection.close()