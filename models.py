from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()
bcript = Bcrypt()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean,default=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')
    
class Parking_Lot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(120), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    occupied = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer,default = True, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    Parking_Spot = db.relationship('Parking_Spot', backref='Parking_Lot',cascade='all, delete-orphan')

class Parking_Spot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    Parking_Lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id',ondelete='CASCADE'), nullable=False)
    

class Parked_History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False,default=datetime.now())
    email = db.Column(db.String(120), nullable=False)
    Parking_Spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id',ondelete='CASCADE'), nullable=False)
    Parking_Lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id',ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(120), nullable=False)

    user = db.relationship('User', backref='Parked_History')
    Parking_Spot = db.relationship('Parking_Spot', backref='Parked_History')
    Parking_Lot = db.relationship('Parking_Lot', backref='Parked_History')