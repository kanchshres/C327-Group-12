# listing.py
from enum import Enum, unique
from multiprocessing.sharedctypes import Value
from qbay.user import User
from qbay.review import Review
from datetime import datetime, timedelta
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

    @property
    def title(self):
        """Fetches title of digital Listing"""
        if self.database_obj:
            self._title = self.database_obj.title
        return self._title

    @title.setter
    def title(self, title):
        """Sets title for digital Listing if valid"""
        if not (Listing.valid_title(title)):
            raise ValueError(f"Invalid Title: {title}")
        self._title = title
        self._modified_date = datetime.now()

    @property
    def description(self):
        """Fetches description of digital Listing"""
        if self.database_obj:
            self._description = self.database_obj.description
        return self._description

    @description.setter
    def description(self, description):
        """Sets title for digital Listing if valid"""
        if not ((20 <= len(description) <= 2000)
                and (len(description) > len(self.title))):
            raise ValueError(f"Invalid Description: {description}")
        self._description = description
        self._modified_date = datetime.now()

    @property
    def price(self):
        """Fetches price of digital Listing"""
        if self.database_obj:
            self._price = self.database_obj.price / 100
        return self._price

    @price.setter
    def price(self, price):
        """Sets price for digital Listing if valid"""
        if not (Listing.valid_price(price) and self.price < price):
            raise ValueError(f"Invalid Price: {price}")
        self._price = price
        self._modified_date = datetime.now()

    @property
    def created_date(self):
        """Fetches last modification date of digital listing"""
        if self.database_obj:
            self._created_date = self.database_obj.date_created
        return self._created_date.date().isoformat()

    @property
    def modified_date(self):
        """Fetches last date modified"""
        if self.database_obj:
            self._modified_date = self.database_obj.last_modified_date
        return self._modified_date.date().isoformat()

    @property
    def seller(self):
        """Fetches owner of digital Listing"""
        return self._seller

    @seller.setter
    def seller(self, owner):
        """Sets owner of digital Listing if valid"""
        if (not Listing.valid_seller(owner)):
            raise ValueError(f"Invalid Seller: {owner}")
        self._seller = owner
        self._modified_date = datetime.now()

    # Extra
    @property
    def address(self):
        """Fetches address of Listing"""
        return self._address

    @address.setter
    def address(self, location):
        """Sets address of Listing"""
        self._address = location
        self._modified_date = datetime.now()

    @property
    def reviews(self) -> 'list[Review]':
        """Fetches reviews of Listing"""
        return self._reviews

    @reviews.setter
    def reviews(self, comments: 'list[Review]'):
        """Sets reviews of Listing"""
        self._reviews = comments

    @property
    def booked_dates(self) -> 'list[str]':
        """Fetches list of booked dates"""
        if self.database_obj:
            result = database.Dates.query.filter_by(listing_id=self.id).all()
            booked_dates = [d.date for d in result]
            return booked_dates
        return None

    def add_review(self, review: 'Review'):
        """Add reviews to listing"""
        self._reviews.append(review)

    def add_to_database(self):
        """Adds listing to the database"""
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
        if not (Listing.valid_price(price)):
            raise ValueError(f"Invalid Price: {price}")
        if not (Listing.valid_description(description, title)):
            raise ValueError(f"Invalid Description: {description}")
            
        listing = Listing(title, description, price, owner, address)
        listing.add_to_database()
        return listing

    @staticmethod
    def valid_title(title):
        """Determine if a given title is valid """
        regex = re.compile(
            r'(^([A-Za-z0-9]([A-Za-z0-9]| ){,78}[A-Za-z0-9])$)|[A-Za-z0-9]')
        if re.fullmatch(regex, title):
            with database.app.app_context():
                exists = database.Listing.query.filter_by(title=title).all()
            return not len(exists)
        return False

    @staticmethod
    def valid_description(description, title):
        """Determine if a given description is valid"""
        return ((19 < len(description) < 2001)
                and (len(title) < len(description)))

    @staticmethod
    def valid_price(price):
        """Determine if a given price is valid"""
        return (10.00 <= price <= 10000.00)

    @staticmethod
    def valid_date(mod_date):
        """Determine if a given last modification date is valid"""
        min_date = datetime(2021, 1, 2)
        max_date = datetime(2025, 1, 2)
        return (min_date < mod_date < max_date)

    @staticmethod
    def valid_seller(owner):
        """Determine if a given owner is valid"""
        if (owner.id):
            with database.app.app_context():
                user = database.User.query.get(owner.id)
                return ((user is not None) and (user.email != ""))
        return False
    
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
        """ Updates the listing price and pushes changes to the 
        database.
        """
        self.price = price

        with database.app.app_context():
            self.database_obj.price = price * 100
            db.session.commit()

    @staticmethod
    def query_listing(id):
        """ Returns a Listing object for interacting with the database
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
        for date in booked_dates:
            date_db = database.Dates(date=date.strftime('%Y-%m-%d'),
                                     listing_id=self.id)
            with database.app.app_context():
                db.session.add(date_db)
                db.session.commit()

    def valid_booking_date(self, booked_dates: list[datetime]):
        """ Check if given booking start and ending dates are valid """
        for date in booked_dates:
            date = date.strftime('%Y-%m-%d')
            if date in self.booked_dates:
                raise ValueError("Given dates overlap with existing bookings!")
        return True

    def find_min_booking_date(self):
        """ Finds the minimum starting date a buyer can book from.
        Helps front end. """
        if self.booked_dates == []:
            return datetime.now().strftime('%Y-%m-%d')
        prev_d = datetime.strptime(self.booked_dates[0], "%Y-%m-%d")
        for i in range(1, len(self.booked_dates)):
            curr_d = datetime.strptime(self.booked_dates[i], "%Y-%m-%d")
            if (curr_d - prev_d).days > 1:
                return curr_d.strftime('%Y-%m-%d')
            prev_d = curr_d
        return (curr_d + timedelta(days=1)).strftime('%Y-%m-%d')