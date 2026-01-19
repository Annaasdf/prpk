from database import db
from flask_login import UserMixin
from datetime import date

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(20))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    meal_type = db.Column(db.String(20))  # breakfast / lunch
    paid = db.Column(db.Boolean, default=False)
    received = db.Column(db.Boolean, default=False)
    order_date = db.Column(db.Date, default=date.today)

class Allergy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True)
    text = db.Column(db.Text)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    text = db.Column(db.Text)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

class PurchaseRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cook_id = db.Column(db.Integer)
    product = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(20), default="pending")
