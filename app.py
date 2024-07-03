from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from faker import Fake
import random

fake=Fake()
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///orders.db'
db=SQLAlchemy(app)

#Define the models 

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    first_name=db.Column(db.String(50), nullable=False)
    last_name=db.Column(db.String(50), nullable=False)
    address=db.Column(db.String(500), nullable=False)
    city=db.Column(db.String(50), nullable=False)
    postcode=db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(50), nullable=False, unique=True)
    orders= db.relationship('Order', backref='customer')


order_product=db.Table('order_product',db.Column('order_id', db.Integer,db.ForeignKey('order.id'),primary_key=True),
                        db.Column('product_id',db.Integer, db.ForeignKey('product.id'),primary_key=True)                         )
                       
class Order(db.Model):  
    id = db.Column(db.Integer, primary_key=True )
    order_date=db.Column(db.DateTime, nullable=False,default=datetime.now)
    shipped_date=db.Column(db.DateTime)
    delivered_date=db.Column(db.DateTime)
    coupon_code=db.Column(db.String(50))
    customer_id=db.Column( db.ForeignKey('customer.id'),nullable=True) 
    products=db.relationship('Product',secondary=order_product)


    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True )
    name= db.Column(db.String(50), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)

def add_customers():
    for _ in range(100):
        customer=Customer(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            address=fake.address(),
            city=fake.city(),
            postcode=fake.postcode(),
            email=fake.email()
        )
        db.session.add(customer)
    db.session.commit()

def add_orders():
    customers=Customer.query.all()# query all the customers first

    #choose a random customer 
    customer=random.choice(customers)
