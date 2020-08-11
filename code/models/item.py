# import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # store_id answers the question: "what store do I belong to?"
    # A foreign key maps values from one table to values in another
    # table.  In this example, Items are mapped to stores, and stores
    # can't be deleted as long as items are linked to it.
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):

        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # (SELECT * FROM items WHERE name=name LIMIT 1)
        
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()

        # if row:                 # returns an object of type ItemModel
        #     return cls(*row)    # same as return cls(row[0], row[1])    (*arg unpacking) 

    def save_to_db(self):   # Serves as both insert and update methods
        db.session.add(self)
        db.session.commit()
        # # The usual database operations... connect, add, commit, close db connection
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        # # The usual database operations... connect, add, commit, close db connection
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()