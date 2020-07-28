# https://flask-restful.readthedocs.io/en/latest/api.html

from flask import Flask, request
from flask_restful import Resource, Api


app = Flask(__name__)
app.secret_key = 'chad'         # obviously this isn't how we'd call our key...    
api = Api(app)

items = []

# Api works with resources, and every resource is a class.
# In this example, Student inherits from Resource and then we
# redefine the built-in get() function.

class Item(Resource):
    def get(self, name):
        
        # for item in items:
        #     if item['name'] == name:
        #         return item

        # this lambda function replaces the above for loop.
        # filter returns a filter object, so we call list() and
        # pass filter for desirable output.  Since there should only
        # be one item in the query, we wrap list in next() to only
        # return first item that matches query. Next() can break our
        # code if the list is empty, so None is also used as a default value.
        item = next(iter(filter(lambda x: x['name'] == name, items)), None)

        # If item not in database:
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(iter(filter(lambda x: x['name'] == name, items)), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        # Get JSON payload from request
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == "__main__":
    app.run(port=5000, debug=True)