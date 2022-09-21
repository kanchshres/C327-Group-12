#user.py
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from wallet import Wallet


class User():
    """ 
    Object representation of a user's account

    params:
    - id: An UID of user's account
    - username: Username for user's account
    - email: Email associated with account
    - password: Password associated with account
    - wallet: Wallet object associated with account
    - review: All the reviews the user has created
    """

    def __init__(self):
        self._id = 0  # should be random unique int, change later
        self._username = ""
        self._email = ""   # should also be unique 
        self._password = ""
        self._wallet = None # user should add balance after account creation
        self._reviews: list['Review'] = []

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        self._username = username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):

        # Check if email is valid
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
            )
        
        if (re.fullmatch(regex, email)):
            self._email = email
        else:
            raise ValueError("Not a valid email address.")
            
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def wallet(self):
        return self._wallet

    @wallet.setter
    def wallet(self, wallet):
        from wallet import Wallet

        if isinstance(wallet, Wallet) or wallet is None:
            self._wallet = wallet
        else:
            raise ValueError("wallet must be an object of type Wallet")

    @property
    def balance(self):
        return self.wallet.balance

    @property
    def reviews(self):
        return self._reviews

    @reviews.setter
    def reviews(self, reviews: list['Review']) -> list['Review']:
        self._reviews = reviews

    def add_review(self, review: 'Review'):
        from review import Review
        if not isinstance(review, Review):
            raise ValueError("Review must be type Review")
        self._reviews.append(review)
