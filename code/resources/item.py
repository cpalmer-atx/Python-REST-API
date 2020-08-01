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
        
        # Add item to db with insert classmethod
        try:
            self.insert(item)
        except:
            return {"message": "An error occured inserting the item."}, 500 # Internal server error  
        return item, 201

    @classmethod
    def insert(cls, item):
        # The usual database operations... connect, add, commit, close db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

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
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}, 500        
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        # The usual database operations... connect, add, commit, close db connection
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()
            
class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = connection.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
            
        connection.close()

        return {'items': items}