# user.py
import sys
from typing import TYPE_CHECKING, List
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc, update, delete, insert, select

from qbay import database
from qbay.database import db

if TYPE_CHECKING:
    from .listing import Listing
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
    - review: All the reviews the user has created
    """

    def __init__(self, username: str = "",
                 email: str = "", password: str = ""):

        self._database_obj: database.User = None
        self._id = None  # created upon being added to database
        self._username: str = username
        self._email: str = email
        self._password = password
        self._postal_code = ""
        self._billing_address = ""
        self._balance = 100
        self._reviews: 'List[Review]' = []
        self._listings_booked: 'List[Listing]' = []

    def __repr__(self):
        return f'<User {self.username}>'

    # Will throw an exception if unique fields not satisfied
    def add_to_database(self):
        """add the user object to the database
        return: True if successful, False otherwise
        """
        user = database.User(username=self.username,
                             email=self.email,
                             password=self.password,
                             postal_code=self.postal_code,
                             billing_address=self.billing_address,
                             balance=self.balance)

        try:
            with database.app.app_context():
                db.session.add(user)
                db.session.commit()
                self._database_obj = user
                self._id = user.id
            return True
        except exc.IntegrityError:
            return False

    @property
    def database_obj(self) -> database.User:
        """Returns a reference to the database"""
        return self._database_obj

    @property
    def id(self):
        """Fetches the user's id"""
        if self.database_obj:
            self._id = self.database_obj.id
        return self._id

    @property
    def username(self) -> str:
        """Fetches the user's username"""
        if self.database_obj:
            self._username = self.database_obj.username
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets a new username, and checks if new username is valid"""
        if not User.valid_username(username):
            raise ValueError(f"Invalid username: {username}")
        self._username = username

    @property
    def email(self) -> str:
        """Fetches the user's email"""
        if self.database_obj:
            self._email = self.database_obj.email
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets a new user email and checks if new email is valid"""
        if not User.valid_email(email):
            raise ValueError(f"Invalid email: {email}")
        self._email = email

    @property
    def password(self) -> str:
        """Fetches the user's password"""
        if self.database_obj:
            self._password = self.database_obj.password
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets a new password, and checks if new password is valid"""
        if not User.valid_password(password):
            raise ValueError(f'Invalid password: {password}')
        self._password = password

    @property
    def balance(self):
        """ Fetches the user's balance """
        if self.database_obj:
            self._balance = self.database_obj.balance
        return self._balance

    @balance.setter
    def balance(self, value):
        """ Set the user's balance """
        self._balance = value

    @property
    def reviews(self):
        """Fetches the list of reviews"""
        return self._reviews

    @reviews.setter
    def reviews(self, reviews: 'List[Review]'):
        """Sets a new list of reviews"""
        self._reviews = reviews

    def add_review(self, review: 'Review'):
        """Adds a review to the list of reviews"""
        self._reviews.append(review)

    @property
    def postal_code(self):
        """Fetches the user's postal code"""
        if self.database_obj:
            self._postal_code = self.database_obj.postal_code
        return self._postal_code

    @postal_code.setter
    def postal_code(self, postal_code: str):
        """Sets a new postal code, and checks that it is valid"""
        regex = re.compile("(?!.*[DFIOQU])[A-VXY][0-9][A-Z][0-9][A-Z][0-9]")
        if re.fullmatch(regex, postal_code):
            self._postal_code: str = postal_code
        else:
            raise ValueError(f"Invalid postal code: {postal_code}")

    @property
    def billing_address(self):
        """Fetches the billing address"""
        if self.database_obj:
            self._billing_address = self.database_obj.billing_address
        return self._billing_address

    @billing_address.setter
    def billing_address(self, bill_addr: str):
        """Sets a new billing address"""
        self._billing_address = bill_addr

    @property
    def listings_booked(self):
        """Fetches the list of listings booked"""
        if self.database_obj:
            self._listings_booked = self.database_obj.listings
        return self._listings_booked
    
    def add_booking(self, booking: 'Listing'):
        """Adds a listing to the list of listings booked"""
        self._listings_booked.append(booking)

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
        if not name:
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
        if not email:
            return False

        regex = re.compile(r"(^[a-zA-Z0-9_.+-]"
                           "+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        return re.fullmatch(regex, email)

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
        """ Register a user and initialize a profile for them only if all 
        requirements are met.
        User's balance is initialized to 100 upon creation

        params:
            name (string):     user name
            email (string):    user email
            password (string): user password

        Returns:
            True if registration succeeded, otherwise False
        """
        # Validate parameters
        if not (User.valid_email(email) and
                User.valid_password(password) and
                User.valid_username(name)):
            return False

        existed = database.User.query.filter_by(email=email).all()
        if len(existed):
            return False

        user = User(username=name, email=email, password=password)

        # add it to current database session
        user.add_to_database()

        return True

    @staticmethod
    def login(email, password):
        """Logs user in if correct corresponding email and password

        Note: other than returning if login was successful or not, 
        logging in doesn't yet give the user any additional features or
        permissions.

        Returns reference to user if login success
        Returns 1 for login failure due to invalid username or password
        Returns 2 for login failure due to incorrect username or 
                                                password (non-matching)
        """
        if not (User.valid_email(email) and User.valid_password(password)):
            raise ValueError("Invalid email or password")
        with database.app.app_context():
            user = database.User.query.filter_by(email=email).first()

            if user:
                if user.password == password:
                    return user

        raise ValueError("Incorrect email or password")

    def update_username(self, username):
        """Updates the user's username and pushes changes to the 
        database (assuming the username isn't already in the database)

        Raises ValueError if the username already exists
        """
        self.username = username
        try:
            self.database_obj.username = username
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            raise ValueError(f"Username already exists: {username}")

    def update_email(self, email):
        """Updates the user's email and pushes changes to the 
        database (if the email isn't already in the database)
        """
        existed = database.User.query.filter_by(email=email).all()
        if len(existed):
            raise ValueError(f"Email already exists: {email}")
        self.email = email
        try:
            self.database_obj.email = email
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()

    def update_billing_address(self, address):
        """Updates the billing address and pushes changes to the 
        database.
        """
        self.billing_address = address
        self.database_obj.billing_address = address
        db.session.commit()

    def update_postal_code(self, postal_code):
        """Updates the postal code and pushes changes to the 
        database.
        """
        self.postal_code = postal_code
        self.database_obj.postal_code = postal_code
        db.session.commit()
    
    def update_balance(self, value):
        """Updates the user's balance and pushes changes to the 
        database.
        """
        self.balance = value
        self.database_obj.balance = value
        db.session.commit()

    @staticmethod
    def query_user(id):
        """Returns an User object for interacting with the database
        in a safe manner. It will initialize a new User object that
        is tethered to the corresponding database object

        Args:
            id (int): integer denoting the unique identifier of the object
            to be queried for

        Returns:
            User: an user object that is tethered to the corresponding
            database object with the given id
        """
        database_user = database.User.query.get(int(id))
        if database_user:
            user = User()
            user._database_obj = database_user
            user.balance = user.database_obj.balance
            return user
        return None
