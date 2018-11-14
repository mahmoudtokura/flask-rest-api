from flask_restful import Resource
from models.storemodel import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {"message": "Store not found"}, 404

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {"message": "Store name taken"}, 400

        store = StoreModel(name=name)

        try:
            store.save_to_db()
        except:
            return {"message": "Error creating store"}, 500

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}

        return {"message": "Store does not exist"}

class StoreList(Resource):
    def get(self):
        stores = StoreModel.query.all()
        return {"Stores": [store.json() for store in stores]}