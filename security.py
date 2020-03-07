from werkzeug.security import safe_str_cmp

from models.user import UserModel


# users = [
#     UserModel(1, 'bob', 'asdf')
# ]
#
# username_mapping = {u.name: u for u in users}
#
# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    #user = username_mapping.get(username, None)

    user = UserModel.find_user_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):

    return UserModel.find_user_by_id(payload['identity'])
