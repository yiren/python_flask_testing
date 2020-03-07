from orm import orm


class UserModel(orm.Model):
    __tablename__ = 'users'
    id = orm.Column(orm.Integer, primary_key=True)
    username = orm.Column(orm.String(80))
    password = orm.Column(orm.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_user_to_db(self):
        orm.session.add(self)
        orm.session.commit()

    def delete_user_in_db(self):
        orm.session.delete(self)
        orm.session.commit()
