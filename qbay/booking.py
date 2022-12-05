# booking.py
from enum import Enum, unique
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Union
from qbay import database
from qbay.database import db
from qbay.user import User
from qbay.listing import Listing
from sqlalchemy import exc


class Booking:
    """Object representation of a listing booking between a buyer and owner

    params:
    - id: ID of the booking (int)
    - owner_id: Listing owner's ID (int)
    - buyer_id: Buyer's ID (int)
    - listing_id: Listing's ID (int)
    - start_date: Starting date of the booking (string)
    - end_date: Ending date of the booking (string)
    """

    def __init__(self, buyer_id: int, owner_id: int, listing_id: int,
                 start_date: str = "", end_date: str = ""):
        self._id = None
        self._owner_id = owner_id
        self._buyer_id = buyer_id
        self._listing_id = listing_id
        self._start_date = start_date
        self._end_date = end_date

    def __str__(self):
        return str(self._id)

    @property
    def id(self):
        return self._id

    @property
    def owner_id(self) -> 'User':
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        self._listing_id = value

    @property
    def buyer_id(self):
        return self._buyer_id

    @buyer_id.setter
    def listing_id(self, value):
        self._listing_id = value

    @property
    def listing_id(self):
        return self._listing_id

    @listing_id.setter
    def listing_id(self, value):
        self._listing_id = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, date: str):
        self._start_date = date
    
    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, date: str):
        self._end_date = date

    @staticmethod
    def book_listing(buyer_id: int, owner_id: int, listing_id: int, 
                     book_start: str, book_end: str):
        """ Book a listing and initialize a profile for them only if all 
        requirements are met.

        params:
        - buyer_id (int): Buyer's ID
        - owner_id (int): Owner's ID
        - listing_id (int): Listing's ID
        - book_start (str): Starting date of the booking
        - book_end (str): Ending date of the booking, exclusive

        Returns:
            True if registration succeeded, otherwise False
        """
        if book_start >= book_end:
            raise ValueError("Start date is the same or after the end date!")

        if buyer_id == owner_id:
            raise ValueError("Owner and buyer are the same!")
        
        buyer = User.query_user(buyer_id)
        listing = Listing.query_listing(listing_id)

        # Get all dates in the booking range given, excluding end date
        # (buyer leaves on final date's morning)
        start = datetime.strptime(book_start, "%Y-%m-%d")
        end = datetime.strptime(book_end, "%Y-%m-%d")
        nights_booked = (end - start).days
        booked_dates = [start + timedelta(days=x)
                        for x in range(0, nights_booked)]

        cost = listing.price * nights_booked
        if buyer.balance < cost:
            raise ValueError("Buyer's balance is too low for this booking!")

        # To book, update listing booking date
        listing.valid_booking_date(booked_dates)
        listing.add_booking_date(booked_dates)

        # Add this listing to buyer's list of bookings
        buyer.add_booking(listing)

        # Update buyer and owner balance
        owner = User.query_user(owner_id)
        buyer.update_balance(buyer.balance - cost)
        owner.update_balance(owner.balance + cost)
        booking = Booking(buyer_id, owner_id, listing_id, book_start, book_end)
        booking.add_to_database()
        return True
    
    def add_to_database(self):
        booking = database.Booking(buyer_id=self.buyer_id,
                                   owner_id=self.owner_id,
                                   listing_id=self.listing_id,
                                   start_date=self.start_date,
                                   end_date=self.end_date)

        try:
            with database.app.app_context():
                db.session.add(booking)
                db.session.commit()
                self._id = booking.id
            return True
        except exc.IntegrityError:
            return False