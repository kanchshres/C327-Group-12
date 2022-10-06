# user.py
from ast import Str
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from qbay.wallet import Wallet
    from qbay.review import Review


"""
This file defines the User profile class
"""


class User():
    """ Object representation of a user's account

    params:
    - id: An UID of user's account
    - username: Username for user's account
    - email: Email associated with account
    - password: Password associated with account
    - postal code: Postal code of user
    - billing address: Billing address of user
    - wallet: Wallet object associated with account
    - review: All the reviews the user has created
    """

    def __init__(self, id=0, username: str = "",
                 email: str = "", password: str = "",
                 postal_code: str = "", billing_address: str = ""):

        self._id = id  # should be random unique int, change later
        self._username: str = username
        self._email: str = email   # should also be unique
        self._password = password
        self._postal_code = postal_code
        self._billing_address = billing_address
        self._wallet: Wallet = None  # user adds wallet after account creation
        self._reviews: 'list[Review]' = []

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = password

    @property
    def wallet(self) -> 'Wallet':
        return self._wallet

    @wallet.setter
    def wallet(self, wallet: 'Wallet'):
        self._wallet = wallet

    def create_wallet(self) -> 'Wallet':
        from qbay.wallet import Wallet
        self._wallet = Wallet()
        return self._wallet

    @property
    def balance(self):
        return self.wallet.balance

    @property
    def reviews(self):
        return self._reviews

    @reviews.setter
    def reviews(self, reviews: 'list[Review]'):
        self._reviews = reviews

    def add_review(self, review: 'Review'):
        self._reviews.append(review)
    
    @property
    def postal_code(self):
        return self._postal_code
    
    @postal_code.setter
    def postal_code(self, pos_code: str):
        self._postal_code = pos_code

    @property
    def billing_address(self):
        return self._billing_address
    
    @billing_address.setter
    def billing_address(self, bill_addr: str):
        self._billing_address = bill_addr

    
def register(name, email, password):
    """ Register a new user

    params:
        name (string):     user name
        email (string):    user email
        password (string): user password
    
    Raises:
        ValueError: When any requirements are not met

    Returns:
        True if registration succeeded, otherwise False
    """

    # R1-1: Email and Password cannot be empty
    if email == "" or password == "":
        return False
        
    # R1-3: Valid email addr-spec
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+'
                       '@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if not (re.fullmatch(regex, email)):
        return False

    # R1-4: Password complexity requirements
    if len(password) < 6:
        return False
    if not (any(c.isupper() for c in password)):
        return False
    if not (any(c.islower() for c in password)):
        return False
    if not (any(not c.isalnum() for c in password)):
        return False

    # R1-5: Username specific requirements
    if name == "":
        return False
    if name[0] == " " or name[-1] == " ":
        return False
    if any(not (c.isalnum() or c == " ") for c in name):
        return False
    
    # R1-6: Username length requirements
    if not (2 < len(name) < 20):
        return False
    
    # R1-7: Email cannot be previously used
    # need database for rest

    # existed = User.query.filter_by(email=email).all()
    # if len(existed) > 0:
    #     return False
    # user = User(username=name, email=email, password=password)
    
    # R1-2: User is identified by unique ID
    # user.id = 

    # R1-8: Billing address is empty
    # R1-9: Postal code is empty

    # R1-10: Balance is 100 at initialization
    # user.wallet.balance = 100

    # # add it to current database session
    # db.session.add(user)
    # # save user object
    # db.session.commit()

    return True