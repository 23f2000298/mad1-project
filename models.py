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


class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(120), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    occupied = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)  # or use Boolean if it's a flag
    price = db.Column(db.Integer, nullable=False)

    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', cascade='all, delete-orphan')
    parked_histories = db.relationship('ParkedHistory', backref='parking_lot', cascade='all, delete-orphan')


class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id', ondelete='CASCADE'), nullable=False) 
    #ondelete='CASCADE' = if we delete parents then child will be deleted

    parked_histories = db.relationship('ParkedHistory', backref='parking_spot', cascade='all, delete-orphan')


class ParkedHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    email = db.Column(db.String(120), nullable=False)
    parking_spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id', ondelete='CASCADE'), nullable=False)
    parking_lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(120), nullable=False)
