from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # The following allows a store to see which items are in items database:
    # 'items' var looks into the ItemModel and sees store_id relationship
    # and determines that 'items' is a LIST of ItemModels.
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
        # There's a performance trade-off between calling json() and creating a store.
        # In this configuration, lazy='dynamic' in line 12 prevents item objects from
        # being created with store creation. This means json() will have to do the lifting
        # when called. You can remove the lazy argument from db.relationship, but then
        # store creation is heavier and all json() calls are for free since db access not needed.
        # For clarity, self.items.all() becomes self.items for this alternative.

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()