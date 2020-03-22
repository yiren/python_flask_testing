from ma import ma
from models.user import UserModel


class UserSchema(ma.Schema):
    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id')
