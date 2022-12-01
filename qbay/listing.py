# listing.py
from enum import Enum, unique
from multiprocessing.sharedctypes import Value
from qbay.user import User
from qbay.review import Review
from datetime import datetime
import re

from qbay import database
from qbay.database import db


class Listing:
    """Object representation of a digital Listing

    params:
    REQUIRED
    - title: Title of listing (string)
    - description: A short description (string)
    - price: The cost of renting the listing (float)
    - date: The last modification date (date)
    - seller: The User associated with the listing (User)

    EXTRA
    - address: The location of the listing (string)
    - reviews: A list of reviews associates with the listing (list[Review])
    """

    """ Initialize digital Listing"""

    def __init__(self, title: str = "", description: str = "",
                 price: float = 0.0, owner: User = User(), address: str = ""):
        # Required
        self._database_obj: database.Listing = None
        self._id = None
        self._title = title
        self._description = description
        self._price = price
        self._created_date: datetime = datetime.now()
        self._modified_date: datetime = datetime.now()
        self._seller = owner
        self._booked_dates = None

        # Extra
        self._address: str = address
        self._reviews: list[Review] = []

    # Required
    @property
    def database_obj(self) -> database.Listing:
        """Returns a reference to the database"""
        return self._database_obj

    @property
    def id(self):
        """Fetches the user's id"""
        if self.database_obj:
            self._id = self.database_obj.id
        return self._id

    """Fetches title of digital Listing"""
    @property
    def title(self):
        if self.database_obj:
            self._title = self.database_obj.title
        return self._title

    """Sets title for digital Listing if valid"""
    @title.setter
    def title(self, title):
        if not (Listing.valid_title(title)):
            raise ValueError(f"Invalid Title: {title}")
        self._title = title
        self._modified_date = datetime.now()

    """Fetches description of digital Listing"""
    @property
    def description(self):
        if self.database_obj:
            self._description = self.database_obj.description
        return self._description

    """Sets title for digital Listing if valid"""
    @description.setter
    def description(self, description):
        if not (Listing.valid_description(description, self.title)):
            raise ValueError(f"Invalid Description: {description}")
        self._description = description
        self._modified_date = datetime.now()

    """Fetches price of digital Listing"""
    @property
    def price(self):
        if self.database_obj:
            self._price = self.database_obj.price / 100
        return self._price

    """Sets price for digital Listing if valid"""
    @price.setter
    def price(self, price):
        if not (Listing.valid_price(price, self.price)):
            raise ValueError(f"Invalid Price: {price}")
        self._price = price
        self._modified_date = datetime.now()

    """Fetches last modification date of digital listing"""
    @property
    def created_date(self):
        if self.database_obj:
            self._created_date = self.database_obj.date_created
        return self._created_date.date().isoformat()

    """Fetches last date modified"""
    @property
    def modified_date(self):
        if self.database_obj:
            self._modified_date = self.database_obj.last_modified_date
        return self._modified_date.date().isoformat()

    """Fetches owner of digital Listing"""
    @property
    def seller(self):
        return self._seller

    """Sets owner of digital Listing if valid"""
    @seller.setter
    def seller(self, owner):
        if not (Listing.valid_seller(owner)):
            raise ValueError(f"Invalid Seller: {owner}")
        self._seller = owner
        self._modified_date = datetime.now()

    """Fetches address of Listing"""
    @property
    def address(self):
        return self._address

    """Sets address of Listing"""
    @address.setter
    def address(self, address):
        if not (Listing.valid_address(address)):
            raise ValueError(f"Invalid Address: {address}")
        self._address = address
        self._modified_date = datetime.now()

    # Extra
    """Fetches reviews of Listing"""
    @property
    def reviews(self) -> 'list[Review]':
        return self._reviews

    """Sets reviews of Listing"""
    @reviews.setter
    def reviews(self, comments: 'list[Review]'):
        self._reviews = comments

    """Fetches list of booked dates"""
    @property
    def booked_dates(self) -> 'list[str]':
        if self.database_obj:
            result = database.Dates.query.filter_by(listing_id=self.id).all()
            booked_dates = [ d.date for d in result ]
            return booked_dates
        return None

    """Add reviews to listing"""
    def add_review(self, review: 'Review'):
        self._reviews.append(review)
        # note: adding a review will currently not update the
        # last_modified_date, since it's not modifying the actual post

    """Adds listing to the database"""
    def add_to_database(self):
        listing = database.Listing(title=self.title,
                                   description=self.description,
                                   price=self.price * 100,
                                   owner_id=self.seller.id,
                                   address=self.address,
                                   date_created=self.created_date,
                                   last_modified_date=self.modified_date)
        with database.app.app_context():
            db.session.add(listing)
            db.session.commit()
            self._database_obj = listing
            self._modified_date = listing.last_modified_date
            self._id = listing.id

    @staticmethod
    def create_listing(title, description, price, owner, address=""):
        """Creates new listing
        Client can not modify the mod_date, rather, it is handled in the 
        server database upon entry update 

        params:
        - title: Title of listing (string)
        - description: A short description (string)
        - price: The cost of renting the listing (float)
        - owner: The User associated with the listing (User)
        - address: The address of the listing (string)
        """
        if not (Listing.valid_title(title)):
            raise ValueError(f"Invalid Title: {title}")
        if not (Listing.valid_seller(owner)):
            raise ValueError(f"Invalid Seller: {owner}")
        if not (Listing.valid_price(price, 0)):
            raise ValueError(f"Invalid Price: {price}")
        if not (Listing.valid_description(description, title)):
            raise ValueError(f"Invalid Description: {description}")
        if not (Listing.valid_address(address)):
            raise ValueError(f"Invalid Address: {address}")
            
        listing = Listing(title, description, price, owner, address)
        listing.add_to_database()
        return listing

    """Determine if a given title is valid """
    @staticmethod
    def valid_title(title):
        regex = re.compile(
            r'(^([A-Za-z0-9]([A-Za-z0-9]| ){,78}[A-Za-z0-9])$)|[A-Za-z0-9]')
        if re.fullmatch(regex, title):
            with database.app.app_context():
                exists = database.Listing.query.filter_by(title=title).all()
            return not len(exists)
        return False

    """Determine if a given description is valid"""
    @staticmethod
    def valid_description(description, title):
        return ((19 < len(description) < 2001)
                and (len(title) < len(description)))

    """Determine if a given price is valid"""
    @staticmethod
    def valid_price(newPrice, oldPrice):
        return ((10.00 <= newPrice <= 10000.00) and (oldPrice < newPrice))

    """Determine if a given last modification date is valid"""
    @staticmethod
    def valid_date(mod_date):
        min_date = datetime(2021, 1, 2)
        max_date = datetime(2025, 1, 2)
        return (min_date < mod_date < max_date)

    """Determine if a given owner is valid"""
    @staticmethod
    def valid_seller(owner):
        if (owner.id):
            with database.app.app_context():
                user = database.User.query.get(owner.id)
                return ((user is not None) and (user.email != ""))
        return False

    """Determine if a given address is valid"""
    @staticmethod
    def valid_address(address):
        return (len(address) <= 46)
    
    def update_title(self, title):
        """Updates the listing title and pushes changes to the 
        database.
        """
        self.title = title
        with database.app.app_context():
            self.database_obj.title = title
            db.session.commit()

    def update_description(self, description):
        """Updates the listing description and pushes changes to the 
        database.
        """
        self.description = description
        with database.app.app_context():
            self.database_obj.description = description
            db.session.commit()

    def update_price(self, price):
        """Updates the listing price and pushes changes to the 
        database.
        """
        self.price = price
        with database.app.app_context():
            self.database_obj.price = price * 100
            db.session.commit()

    def update_address(self, address):
        """Updates the listing address and pushes changes to the 
        database.
        """
        self.address = address
        with database.app.app_context():
            self.database_obj.address = address
            db.session.commit()

    @staticmethod
    def query_listing(id):
        """Returns a Listing object for interacting with the database
        in a safe manner. It will initialize a new User object that
        is tethered to the corresponding database object

        Args:
            id (int): integer denoting the unique identifier of the object
            to be queried for

        Returns:
            Listing: a listing object that is tethered to the corresponding
            database object with the given id
        """
        database_listing = database.Listing.query.get(int(id))
        if database_listing:
            listing = Listing()
            listing._database_obj = database_listing
            return listing
        return None

    def add_booking_date(self, booked_dates: list[datetime]):
        """ Adds booked dates to list of bookings """
        with database.app.app_context():
            for date in booked_dates:
                date_db = database.Dates(date=date.strftime('%Y-%m-%d'),
                                        listing_id=self.id)
                db.session.add(date_db)
            db.session.commit()

    def valid_booking_date(self, booked_dates: list[datetime]):
        """ Check if given booking start and ending dates are valid """
        print(self.booked_dates)
        for date in booked_dates:
            date = date.strftime('%Y-%m-%d')
            print(date)
            if date in self.booked_dates:
                raise ValueError("Given dates overlap with existing bookings!")
        return True
