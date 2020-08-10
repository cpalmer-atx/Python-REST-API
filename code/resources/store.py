from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    # GET
    def get(self, name):
        pass

    # POST
    def post(self, name):
        pass
    # DELETE
    
    def delete(self, name):
        pass

class StoreList(Resource):
    pass