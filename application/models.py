from .database import db
from datetime import datetime


class User(db.Model):
    id  = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(),unique = True,nullable = False)
    email = db.Column(db.String(),unique = True,nullable = False)
    password = db.Column(db.String(),nullable = False)
    type = db.Column(db.String(),default = "general")
    parkinglot = db.relationship("ParkingLot",backref = "bearer")

   

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_no = db.Column(db.String(80), nullable=False)
    spot_id = db.Column(db.Integer, nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey("parking_lot.id"),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable = False)
    parking_time = db.Column(db.DateTime,default = datetime.utcnow)
    release_time = db.Column(db.DateTime,nullable = True)
    total_cost = db.Column(db.Float,nullable = True)
    available = db.Column(db.Boolean,default = True) 

    
class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(80), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Integer, nullable=False)
    maximum_spot = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable = False)
    bookings = db.relationship("Booking",backref = "parking_lot",cascade = "all",passive_deletes = True)