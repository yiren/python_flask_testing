from typing import Dict, Union

from orm import orm

UserJson = Dict[str, Union[int, str]]


class UserModel(orm.Model):
    __tablename__ = 'users'
    id = orm.Column(orm.Integer, primary_key=True)
    username = orm.Column(orm.String(80))
    password = orm.Column(orm.String(80))

    def __init__(self, username:str, password:str):
        self.username = username
        self.password = password

    def json(self) -> Dict:
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

    def save_user_to_db(self) -> None:
        orm.session.add(self)
        orm.session.commit()

    def delete_user_in_db(self) -> None:
        orm.session.delete(self)
        orm.session.commit()
