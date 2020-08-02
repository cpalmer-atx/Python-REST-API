from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
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
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    
    def post(self, name):       # CREATE

        # First check to see if the new item already exists
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        # Get JSON payload from request
        item = ItemModel(name, data['price'])
        
        # Add item to db with insert classmethod
        try:
            item.insert()
        except:
            return {"message": "An error occured inserting the item."}, 500 # Internal server error  
        return item.json(), 201

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
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500        
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item.json()

            
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