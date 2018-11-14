#This is the User Model File.

import sqlite3
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


    def __init__(self, name, password):
        self.name = name
        self.password = password


    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(name=username).first()


    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()