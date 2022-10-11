# user.py
from typing import TYPE_CHECKING
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from qbay import database
from qbay.database import db
from qbay.wallet import Wallet, BankingAccount

if TYPE_CHECKING:
    from .wallet import Wallet
    from .review import Review


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

    def __init__(self, username: str = "",
                 email: str = "", password: str = "",
                 postal_code: str = "", billing_address: str = ""):

        self._id = None
        self._username: str = username
        self._email: str = email
        self._password = password
        self._postal_code = postal_code
        self._billing_address = billing_address
        self._wallet: Wallet = None  # user adds wallet after account creation
        self._reviews: 'list[Review]' = []

    def __repr__(self):
        return f'<User {self.username}>'

    def add_to_database(self):
        user = database.User(username=self.username,
                             email=self.email,
                             password=self.password,
                             wallet=self.wallet or None,
                             postal_code=self.postal_code,
                             billing_address=self.billing_address)
        with database.app.app_context():
            db.session.add(user)
            db.session.commit()
            self._id = user.id

    def update_username(self, username) -> bool:
        try:
            self.username = username
        except ValueError as e:
            print(e)
            return False

    @property
    def id(self):
        return self._id

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str):
        if not User.valid_username(username):
            raise ValueError(f"Invalid username: {username}")
        self._username = username

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        if not User.valid_email(email):
            raise ValueError(f"Invalid email: {email}")
        self._email = email


    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        if not User.valid_password(password):
            raise ValueError(f'Invalid password: {password}')
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

    @staticmethod
    def valid_username(name):
        """ Checks to see if given username follows requirements R1-5 and R1-6
        R1-5: Username cannot be empty, have spaces as a prefix or suffix, and 
            can only consist of alphanumeric characters.
        R1-6: Username must be between 2 and 20 characters in length.

        params:
            name (string): user name

        Returns:
            True if user name is valid, False if not
        """
        if name == "":
            return False
        if name[0] == " " or name[-1] == " ":
            return False
        if any(not (c.isalnum() or c == " ") for c in name):
            return False
        if not (2 < len(name) < 20):
            return False
        return True

    @staticmethod
    def valid_email(email):
        """ Checks to see if email follows requirements R1-1 and R1-3
        R1-1: Email is not empty.
        R1-3: Email follows addr-spec from RFC 5322.

        params:
            email (string): user email

        Returns:
            True if email is valid, False if not
        """
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+'
                           '@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not (re.fullmatch(regex, email)):
            return False
        return True

    @staticmethod
    def valid_password(password):
        """ Check if given password follows requirements R1-2 and R1-4
        R1-1: Password is not empty.
        R1-4: Password cannot be shorter than 6 characters, and requires at 
              least one upper case, lower case, and special character.

        params:
            password (string): user password

        Returns:
            True if password is valid, False if not
        """
        if password == "":
            return False
        if len(password) < 6:
            return False
        if not (any(c.isupper() for c in password)):
            return False
        if not (any(c.islower() for c in password)):
            return False
        if not (any(not c.isalnum() for c in password)):
            return False
        return True

    @staticmethod
    def register(name, email, password):
        """ Register a user and initialize a profile for them only if all 
        requirements are met.

        params:
            name (string):     user name
            email (string):    user email
            password (string): user password

        Returns:
            True if registration succeeded, otherwise False
        """
        # Validate parameters
        if (not User.valid_email(email)):
            return False
        if (not User.valid_password(password)):
            return False
        if (not User.valid_username(name)):
            return False

        existed = database.User.query.filter_by(email=email).all()
        if len(existed) > 0:
            return False
        user = User(username=name, email=email, password=password)
        wallet = Wallet()
        wallet.bankingAccount = BankingAccount()
        wallet.bankingAccount.add_balance(100)
        user.wallet = wallet.id

        # add it to current database session
        user.add_to_database()

        return True
