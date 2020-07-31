from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):

    # Tool to parse all requests
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Item price cannot be left blank."
    )

    
    @jwt_required()
    def get(self, name):        #READ
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    
    def post(self, name):       # CREATE

        # First check to see if the new item already exists
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # Get JSON payload from request
        item = {'name': name, 'price': data['price']}

        # The usual database operations... connect, add, commit, close db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()
        
        return item, 201

    def delete(self, name):     #DELETE

        # The usual database operations... connect, add, commit, close db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': "{} deleted".format(name)}

    def put(self, name):        # UPDATE

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