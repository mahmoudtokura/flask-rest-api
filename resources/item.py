import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.itemmodel import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, help='Add a price', required=True)
    parser.add_argument('store_id', type=int, help='Add a store id', required=True)


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": "Item does not exists"}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name {name} already exist"}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data) # The same as ItemModel(name, "price": data['price'], store_id: data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "Error while inserting"}, 500

        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted"}
        return {"message": "Item does not exist"}, 400

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        try:
            if item is None:
                item = ItemModel(name, **data)
                item.save_to_db()
                return item.json(), 201
            else:
                item.price = data['price']
                item.save_to_db()
                return item.json, 202
        except:
            return {"message": "Error while creating new Item"}, 500


class ItemList(Resource):
    def get(self):
        items = ItemModel.query.all()
        return {'items': [item.json() for item in items]}, 200
