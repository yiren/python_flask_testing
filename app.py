from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'message': 'Hello World'})


if __name__ == '__main__': # Only called when running 'app.py,' running not from imports
    app.run()