from flask_sqlalchemy import SQLAlchemy #for designing the database
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcript = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean,default=False)

    def __init__(self, name, email, password, admin):
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')
        
       