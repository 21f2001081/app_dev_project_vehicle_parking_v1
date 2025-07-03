from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app

db=SQLAlchemy()

class Admin(db.Model):
    __tablename__ = "Admin"
    id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True )
    username = db.Column(db.String(64), nullable = False, unique=True )
    passhash =  db.Column(db.String(64), nullable = False )
    full_name = db.Column(db.String(128), nullable = False )
    address = db.Column(db.String(512), nullable = False )
    pincode = db.Column(db.Integer, nullable = False )
    
    def set_password(self, password):
        self.passhash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.passhash, password)
    
class Parking_lot(db.Model):
    __tablename__ = "Parking_lot"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True )
    location = db.Column(db.String(64), nullable = False, unique=True )
    address = db.Column(db.String(512), nullable = False )
    pincode = db.Column(db.Integer, nullable = False )
    price = db.Column(db.Integer, nullable = False )
    max_no_spots = db.Column(db.Integer, nullable = False )
    landmark = db.Column(db.String(64), nullable = False )
    
    
class Parking_spot(db.Model):
    __tablename__ = "Parking_spot"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True )
    parking_lot_id = db.Column(db.Integer, db.ForeignKey("Parking_lot.id"), nullable = False )
    is_booked = db.Column(db.Boolean, default=False)
    additional_info = db.Column(db.String(64), nullable=True)
    
    parking_lot = db.relationship("Parking_lot", backref=db.backref("parking_spots", lazy=True, cascade ="all, delete"))
    
class Booking(db.Model):
    __tablename__ = "Booking"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True )
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable = False )
    parking_spot_id = db.Column(db.Integer, db.ForeignKey("Parking_spot.id"), nullable = False )
    vehicle_number = db.Column(db.String(20), nullable = False )
    start_time = db.Column(db.DateTime, nullable = False )
    end_time = db.Column(db.DateTime, nullable = False )
    cost = db.Column(db.Integer, nullable = False )
    
    user = db.relationship("User", backref=db.backref("bookings", lazy=True, cascade ="all, delete"))
    parking_spot = db.relationship("Parking_spot", backref=db.backref("bookings", lazy=True, cascade ="all, delete"))
    