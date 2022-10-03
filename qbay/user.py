#user.py
from ast import Str
from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from wallet import Wallet
    from review import Review


class User():
    """ Object representation of a user's account

    params:
    - id: An UID of user's account
    - username: Username for user's account
    - email: Email associated with account
    - password: Password associated with account
    - wallet: Wallet object associated with account
    - review: All the reviews the user has created
    """

    def __init__(self, id = 0, username: str = ""
                , email: str = "", password: str = ""
                , postal_code: str = "", billing_address: str = ""):
        self._id = id  # should be random unique int, change later
        self._username: str = username
        self._email: str = email   # should also be unique 
        self._password = password
        self._postal_code = postal_code
        self._billing_address = billing_address
        self._wallet: Wallet = None # user adds wallet after account creation
        self._reviews: 'list[Review]' = []

    def __repr__(self):
        return '<User' % self.username
        
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

        # Check if email is valid
        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
            )
        
        if (re.fullmatch(regex, email)):
            self._email = email
        else:
            raise ValueError("Not a valid email address.")
            
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
        from wallet import Wallet
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
    
    def register(name, email, password):
        # R1-1: Email and Password cannot be empty
        if email == "" or password == "":
            raise ValueError("Username/password cannot be empty.")

        # R1-4: Password complexity requirements
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        if not (any(c.isupper() for c in password)):
            raise ValueError("Password must have at least one uppercase letter.")
        if not (any(c.islower() for c in password)):
            raise ValueError("Password must have at least one lowercase letter.")
        if not (any(not c.isalnum() for c in password)):
            raise ValueError("Password must have at least one special character.")

        # R1-5: Username specific requirements
        if name == "":
            raise ValueError("Username cannot be empty")
        if name[0] == " " or name[-1] == " ":
            raise ValueError("Username cannot have space as prefix or suffix")
        if any(not c.isalnum() for c in name):
            raise ValueError("Username cannot have special characters")
        
        # R1-6: Username length requirements
        if not ( 2 < len(name) < 20):
            raise ValueError("Username must be between 2 and 20 characters in length")
        
        # R1-7: Email cannot be previously used
        existed = User.query.filter_by(email=email).all()
        if len(existed) > 0:
            return False
        user = User(username = name, email = email, password = password)
        # R1-2: User is identified by unique ID
        #user.id = 
        # R1-8: Billing address is empty
        # R1-9: Postal code is empty
        # R1-10: Balance is 100 at initialization

        return True

    def login(email, password):
        # R2-2
        valids = User.query.filter_by(email=email, password=password).all()
        if len(valids) != 1:
            return None
        # R2-1
        return valids[0]
 