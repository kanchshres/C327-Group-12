# user.py
from ast import Str
import sys
from typing import TYPE_CHECKING
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

from qbay import database, wallet
from qbay.database import db

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

        self._id = None  # should be random unique int, change later
        self._username: str = username
        self._email: str = email   # should also be unique
        self._password = password
        self._postal_code = postal_code
        self._billing_address = billing_address
        self._wallet: Wallet = None  # user adds wallet after account creation
        self._reviews: 'list[Review]' = []

    def __repr__(self):
        return f'<User {self.username}>'

    # Will throw an exception if unique fields not satified
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
        # try:
        #     db.session.add(user)
        #     db.session.commit()
        #     self._id = user.id
        #     return self.id
        # except exc.IntegrityError as e:
        #     print(f'Object exists in database, error: {e}', file=sys.stderr)

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
        regex = re.compile(r"^[A-Za-z]+( +[A-Za-z])*[A-Za-z]*")
        if (2 < len(username) < 20) and re.fullmatch(regex, username):
            self._username = username
        else:
            raise ValueError("Invalid username: %r" % username)

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
        if email == "":
            return False

        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+'
                           '@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not (re.fullmatch(regex, email)):
            return False
        return True

    @staticmethod
    def valid_password(password):
        """ Check if given password follows requirements R1-2 and R1-4
        R1-1: Password is not empty.
        R1-4: Password cannot be shorter than 6 characters, and requires
            at least one upper case, lower case, and special character.

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
        """ Register a new user

        params:
            name (string):     user name
            email (string):    user email
            password (string): user password

        Returns:
            True if registration succeeded, otherwise False
        """

        # R1-1: Email cannot be empty
        # R1-3: Valid email addr-spec
        if not User.valid_email(email):
            return False

        # R1-1: Password cannot be empty
        # R1-4: Password complexity requirements
        if not User.valid_password(password):
            return False

        # R1-5: Username specific requirements
        # R1-6: Username length requirements
        if not User.valid_username(name):
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

    @staticmethod
    def login(username, password):
        """Logs user in if correct corresponding username and password

        Note: other than returning if login was successful or not, 
        logging in doesn't yet give the user any additional features or
        permissions.

        Returns 0 for login success
        Returns 1 for login failure due to invalid username or password
        Returns 2 for login failure due to incorrect username or 
                                                password (non-matching)
        """
        if not (User.valid_username(username) and User.valid_password(password)):
            return 1

        for i in db.session.execute(db.select(users).filter(db.users.username == username)).all():
            if i.password == password:
                # login
                return 0
        return 2