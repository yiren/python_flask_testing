from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)

api= Api(app)

class Student(Resource):
    def get(self, name):
        return {'student': name}

api.add_resource(Student, '/student/<string:name>')


if __name__ == '__main__': # Only called when running 'app.py,' running not from imports
    app.run(debug=True, port=5001)