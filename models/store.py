from typing import Dict, List
from orm import orm


class StoreModel(orm.Model):
    __tablename__ = 'stores'
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(80))
    items = orm.relationship('ItemModel', lazy="dynamic")

    def __init__(self, name: str):
        self.name = name

    def json(self) -> Dict:
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod  # notice that this cannot be changed to class function/method but should be @classmethod
    def find_store_by_name(cls, name:str):
        return cls.query.filter_by(name=name).first()

    def save_store_to_db(self) -> None:
        orm.session.add(self)
        orm.session.commit()

    def delete_store_in_db(self) -> None:
        orm.session.delete(self)
        orm.session.commit()

    @classmethod
    def get_stores_from_db(cls) -> List:
        return cls.query.all()
    # def update_item_to_db(self):
    #     connection = sqlite3.connect('data.db')
    #     cursor = connection.cursor()
    #     update_query = 'update items set price =? where name=?'
    #     cursor.execute(update_query, (self.price, self.name,))
    #     connection.commit()
    #     connection.close()
