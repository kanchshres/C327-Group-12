# booking.py
from enum import Enum, unique

from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
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
        self._user_id = None
        self._listing_id = None
        self._price: 'float' = 0
        self._date = ""
    
    def __str__(self):
        return str(self._id)
    
    @property
    def id(self):
        return self._id

    @property
    def user_id(self) -> 'User':
        return self._user_id
    
    @user_id.setter
    def payer(self, value):
        self._payer = value

    @property
    def listing_id(self):
        return self._list_id
    
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
        