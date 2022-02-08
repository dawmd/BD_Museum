from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Institution(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))

class Employee(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    institution = db.Column(db.Integer)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150))
    birth_date = db.Column(db.DateTime(timezone = True))
    death_date = db.Column(db.DateTime(timezone = True))

class Exhibit(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.Integer)
    localization = db.Column(db.Integer)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    x_size = db.Column(db.Integer)
    y_size = db.Column(db.Integer)
    z_size = db.Column(db.Integer)
    state = db.Column(db.Integer)

class History(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.Integer)
    borrower = db.Column(db.Integer)
    beginning = db.Column(db.DateTime(timezone = True), default = func.now())
    end = db.Column(db.DateTime(timezone = True))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
