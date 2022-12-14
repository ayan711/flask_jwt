# from . import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   public_id = db.Column(db.Integer)
   name = db.Column(db.String(50))
   password = db.Column(db.String(50))
   admin = db.Column(db.Boolean)

class Books(db.Model):
    
   id = db.Column(db.Integer, primary_key=True)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
   name = db.Column(db.String(50), unique=True, nullable=False)
   Author = db.Column(db.String(50), unique=True, nullable=False)
   Publisher = db.Column(db.String(50), nullable=False)
   book_prize = db.Column(db.Integer)
   created_at = db.Column(db.DateTime, default=datetime.now())
   updated_at = db.Column(db.DateTime, onupdate=datetime.now())
