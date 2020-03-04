import sqlite3
from orm import orm
class UserModel(orm.Model):
    __tablename__ ='users'
    id = orm.Column(orm.Integer, primary_key=True)
    username = orm.Column(orm.String(80))
    password = orm.Column(orm.String(80))

    def __init__(self, _id, name, password):
        self.id = _id
        self.name = name
        self.password = password

    @classmethod
    def find_user_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'select * from users as u where u.username = ?'
        row = cursor.execute(query, (username,))
        result = row.fetchone()
        if result:
            user = cls(*result)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_user_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'select * from users as u where u.id = ?'
        row = cursor.execute(query, (_id,))
        result = row.fetchone()
        if result:
            user = cls(*result)
        else:
            user = None
        connection.close()
        return user
