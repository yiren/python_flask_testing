from app import app
from ma import ma
from orm import orm


@app.before_first_request
def create_tables():
    orm.create_all()


orm.init_app(app)

ma.init_app(app)
app.run(debug=True, port=5001)
