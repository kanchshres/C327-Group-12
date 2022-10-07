import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'qbay_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    wallet = db.Column(db.Integer, nullable=True) #Changing it to wallet_id breaks it
    postal_code = db.Column(db.String(7), nullable=True)
    billing_address = db.Column(db.String(46), nullable=True)

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Listing(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.String(5000), nullable=False)
    price = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    last_modified_date = db.Column(db.String(20), nullable=True)
    owner_id = db.Column(db.Integer(), nullable=True)
    
    def __repr__(self) -> str:
        return f'<Listing {self.title}>'


class Review(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    listing_id = db.Column(db.Integer(), nullable=False)
    review_text = db.Column(db.String(5000), nullable=True)
    date = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self) -> str:
        return f'<Review {self.id}>'


class Booking(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), nullable=False)
    listing_id = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    last_modified_date = db.Column(db.String(20), nullable=True)
    
    def __repr__(self) -> str:
        return f'<Booking {self.id}>'

class Wallet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    balance = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    bankingAccount = db.Column(db.Integer(), nullable=False)
    #transactions = db.Column(db.ARRAY(db.Integer()), nullable=True)

    def __repr__(self) -> str:
        return f'<Wallet {self.id}>'
    
class Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    payer_id= db.Column(db.Integer(), nullable=False)
    payee_id = db.Column(db.Integer(), nullable=False)
    amount = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    booking = db.Column(db.Integer(), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    
    def __repr__(self) -> str:
        return f'<Transaction {self.id}>'
