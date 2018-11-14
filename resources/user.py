import sqlite3
from flask_restful import Resource, reqparse
from models.usermodel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='Must add username', required=True)
    parser.add_argument('password', type=str, help='Must add password', required=True)

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"This username is taken"}, 400

        user = UserModel(data['username'],data['password'])
        user.save_to_db()

        return {"message": "User created successfully"}, 201