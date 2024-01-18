from flask_login import UserMixin

from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), unique = True)
    username = db.Column(db.String(200), unique=True)
    firstName = db.Column(db.String(200))
    lastName = db.Column(db.String(200))
    password = db.Column(db.String(200))
    recipes = db.Column(db.Text)
    #name~link~img_src`name~link~img_src`etc




