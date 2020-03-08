from app_restful import app
from orm import orm

orm.init_app(app)


@app.before_first_request
def create_tables():
    orm.create_all()
