from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
# import sqlite3

class Item(Resource):

    # Tool to parse all requests
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Every item needs a store id."
    )
    parser.add_argument('store_id',
        type=int,
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
        item = ItemModel(name, data['price'], data['store_id'])
        
        # Add item to db with insert classmethod
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500 # Internal server error  
        return item.json(), 201

    def delete(self, name):     #DELETE
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

        # # The usual database operations... connect, add, commit, close db connection
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()

        # return {'message': "{} deleted".format(name)}

    def put(self, name):        # UPDATE
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            # try:
            #     updated_item.save_to_db()
            # except:
            #     return {"message": "An error occurred inserting the item."}, 500        
        else:
            item.price = data['price']
            # try:
            #     updated_item.delete_from_db()
            # except:
            #     return {"message": "An error occurred updating the item."}, 500
        item.save_to_db()
        return item.json()

            
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = connection.execute(query)
        # items = []
        # for row in result:
        #     items.append({'name': row[0], 'price': row[1]})
            
        # connection.close()

        # return {'items': items}