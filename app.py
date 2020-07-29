from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity
from user import UserRegister


app = Flask(__name__)
app.secret_key = 'chad'                 # obviously this isn't how we'd call our key...
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []

class Item(Resource):

    # Tool to parse all requests
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Item price cannot be left blank."
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)

        # If item not in database:
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()     # calling parser tool defined at begining of Item class

        # Get JSON payload from request
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items

        # Function overwrites existing items list excluding item to delete
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': '{} deleted'.format(name)}

    def put(self, name):

        data = Item.parser.parse_args()     # calling parser tool defined at begining of Item class
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item
            
class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')


if __name__ == "__main__":
    app.run(port=5000, debug=True)