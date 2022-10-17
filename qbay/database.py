import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, Table
import sqlalchemy.types
from sqlalchemy.orm import relationship

import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'qbay_database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '69cae04b04756f65eabcd2c5a11c8c24'

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(7), nullable=True)
    billing_address = db.Column(db.String(46), nullable=True)

    wallet = relationship('Wallet', back_populates='user', uselist=False)
    listings = relationship('Listing', back_populates='owner')
    reviews = relationship('Review', back_populates='user')
    bookings = relationship('Booking', back_populates='user')

    def __repr__(self) -> str:
        return f'<User {self.username}>'


class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    price = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    time_created = db.Column(db.DateTime(timezone=False),
                             server_default=func.now())
    last_modified_date = db.Column(db.DateTime(timezone=False),
                                   onupdate=func.now())

    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))
    owner = relationship('User', back_populates='listings')

    reviews = relationship('Review', back_populates='listing')

    bookings = relationship('Booking', back_populates='listing')

    def __repr__(self) -> str:
        return f'<Listing {self.title}>'


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    review_text = db.Column(db.String(5000), nullable=True)
    date = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = relationship('User', back_populates='reviews')

    listing_id = db.Column(db.Integer, db.ForeignKey(Listing.id))
    listing = relationship('Listing', back_populates='reviews')

    def __repr__(self) -> str:
        return f'<Review {self.id}>'


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listing_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    last_modified_date = db.Column(db.String(20), nullable=True)

    user_id = db.Column(db.Integer(), db.ForeignKey(User.id))
    user = relationship('User', back_populates='bookings')

    listing_id = db.Column(db.Integer, db.ForeignKey(Listing.id))
    listing = relationship('Listing', back_populates='bookings')

    def __repr__(self) -> str:
        return f'<Booking {self.id}>'


class BankingAccount(db.Model):
    __tablename__ = 'banking_accounts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    balance = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)

    def __repr__(self) -> str:
        return f'<BankingAccount {self.id}>'


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    balance = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = relationship('User', back_populates='wallet')

    transactions = relationship(
        'Transaction', primaryjoin="Wallet.id==Transaction.payer_id")

    banking_account_id = db.Column(
        db.Integer, db.ForeignKey(BankingAccount.id))
    banking_account = relationship('BankingAccount')

    def __repr__(self) -> str:
        return f'<Wallet {self.id}>'


class Transaction(db.Model):
    __tablename__ = 'transaction'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    status = db.Column(db.String(30), nullable=False)

    payer_id = db.Column(db.Integer, db.ForeignKey(Wallet.id))
    payer = relationship(
        'Wallet', foreign_keys=[payer_id], back_populates='transactions')

    payee_id = db.Column(db.Integer, db.ForeignKey(Wallet.id))
    payee = relationship('Wallet', foreign_keys=[payee_id])

    booking_id = db.Column(db.Integer, db.ForeignKey(Booking.id))
    booking = relationship('Booking')

    def __repr__(self) -> str:
        return f'<Transaction {self.id}>'
