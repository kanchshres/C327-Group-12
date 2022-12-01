# booking.py
from enum import Enum, unique
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Union
from qbay import database
from qbay.database import db, app
from qbay.user import User
from qbay.listing import Listing
from qbay.transaction import Transaction


class Booking:
    """Object representation of a transaction between two users

    params:
    - ID: The transaction id.
    - payer: Type User who is responsible for making the payment
    - payee: Type User who is receiving the payment
    - amount: The amount to be transferred
    - listing: Type Listing as the subject of the transaction
    - status: Type TransactionStatus()
    """

    def __init__(self):
        self._id = None
        self._owner_id = None
        self._listing_id = None
        self._date = ""

    def __str__(self):
        return str(self._id)

    @property
    def id(self):
        return self._id

    @property
    def owner_id(self) -> 'User':
        return self._owner_id

    @owner_id.setter
    def payer(self, value):
        self._payer = value

    @property
    def listing_id(self):
        return self._listing_id

    @listing_id.setter
    def listing_id(self, value):
        self._listing_id = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @staticmethod
    def book_listing(buyer_id: int, owner_id: int, listing_id: int, 
                     book_start: str, book_end: str):
        """ Books listing for a buyer"""
        if buyer_id == owner_id:
            raise ValueError("Owner and buyer are the same!")
        
        buyer = User.query_user(buyer_id)
        listing = Listing.query_listing(listing_id)

        # Get all dates in the booking range given
        start = datetime.strptime(book_start, "%Y-%m-%d")
        end = datetime.strptime(book_end, "%Y-%m-%d")
        days_booked = (end - start).days
        booked_dates = [start + timedelta(days=x)
                        for x in range(0, days_booked + 1)]
        
        cost = listing.price * days_booked
        if buyer.balance < cost:
            raise ValueError("Buyer's balance is too low for this booking!")

        # To book, update listing booking date
        listing.valid_booking_date(booked_dates)
        listing.add_booking_date(booked_dates)

        # Add this listing to buyer's list of bookings
        buyer.add_booking(listing)

        # Update buyer and owner balance
        owner = User.query_user(owner_id)
        buyer.balance = buyer.balance - cost
        owner.balance = owner.balance + cost
        # Add to database
        Booking.add_to_database(owner_id, listing_id, book_start, book_end)
    
    def add_to_database(owner_id, listing_id, start, end):
        booking = database.Booking(owner_id=owner_id, 
                                   listing_id=listing_id,
                                   start_date=start,
                                   end_date=end)

        with database.app.app_context():
            db.session.add(booking)
            db.session.commit()
        
