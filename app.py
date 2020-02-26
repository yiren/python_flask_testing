from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
        {
            'name': 'My First Store',
            'items': [
                {
                    'name': 'My First Item',
                    'price': 15.99
                }
            ]
        }
]

@app.route('/')
def home():
    return jsonify({'message': 'Hello World'})

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(stores)

@app.route('/store')
def get_stores():
    return jsonify(stores)

@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'store not found'})

@app.route('/store/<string:name>/item', methods=['POST'])
def create_item(name):
    for store in stores:
        if store['name'] == name:
            request_data= request.get_json()
            new_item={
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(store)
    return jsonify({'message': 'store not found'})



if __name__ == '__main__': # Only called when running 'app.py,' running not from imports
    app.run(debug=True)