# listing.py
from enum import Enum, unique
from multiprocessing.sharedctypes import Value
from qbay.user import User
from qbay.review import Review
from datetime import datetime


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
                 price: float = 0.0, owner=User(), address: str = ""):
        # Required
        self._title = title
        self._description = description
        self._price = price
        self._date = None
        self._seller = owner

        # Extra
        self._address: str = address
        self._reviews: list[Review] = []

    # Required
    """Fetches title of digital Listing"""
    @property
    def title(self):
        return self._title

    """Sets title for digital Listing"""
    @title.setter
    def title(self, title):
        if (not Listing.valid_title(title)):
            raise ValueError(f"Invalid Title: {title}")
        self._title = title

    """Fetches description of digital Listing"""
    @property
    def description(self):
        return self._description

    """Sets title for digital Listing"""
    @description.setter
    def description(self, description, title):
        if (not Listing.valid_description(description, title)):
            raise ValueError(f"Invalid Description: {description}")
        self._description = description

    """Fetches price of digital Listing"""
    @property
    def price(self):
        return self._price

    """Sets price for digital Listing"""
    @price.setter
    def price(self, price):
        if (not Listing.valid_price(price)):
            raise ValueError(f"Invalid Price: {price}")
        self._price = price

    """Fetches last modification date of digital listing"""
    @property
    def date(self):
        return self._date

    """Updates last modification date of digital listing"""
    @date.setter
    def date(self, mod_date):
        if (not Listing.valid_date(mod_date)):
            raise ValueError(f"Invalid Date: {mod_date}")
        self._date = mod_date

    """Fetches owner of digital Listing"""
    @property
    def seller(self):
        return self._seller

    """Sets owner of digital Listing"""
    @seller.setter
    def seller(self, owner):
        if (not Listing.valid_seller(owner)):
            raise ValueError(f"Invalid Seller: {owner}")
        self._seller = owner

    # Extra
    """Fetches address of Listing"""
    @property
    def address(self):
        return self._address

    """Sets address of Listing"""
    @address.setter
    def address(self, location):
        self._address = location
    
    """Fetches reviews of Listing"""
    @property
    def reviews(self) -> 'list[Review]':
        return self._reviews

    """Sets reviews of Listing"""
    @reviews.setter
    def reviews(self, comments: 'list[Review]'):
        self._reviews = comments

    """Add reviews to listing"""

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    """Create a new listing - return true of succssfull and false otherwise"""
    @staticmethod
    def create_listing(title, description, price, mod_date, owner):
        if (Listing.valid_title(title) and Listing.valid_seller(owner) and
                Listing.valid_price(price) and Listing.valid_date(mod_date) and
                Listing.valid_description(description, title)):
            listing = Listing(title, description, price, owner)
            # Commit to database as well
            return True
        return False

    """Determine if a given title is valid """
    @staticmethod
    def valid_title(title):
        validation_status = False

        # Validate title has maximum 80 characters and prefix/suffix of not ' '
        if ((len(title) < 81) and (title[0] != ' ') and (title[-1] != ' ')):

            # Validate title only contains alphanumeric or 'space' characters
            passed = True
            for c in title:
                valid_char = False
                if ((47 < ord(c) < 58)):
                    valid_char = True
                elif ((64 < ord(c) < 91)):
                    valid_char = True
                elif ((96 < ord(c) < 123)):
                    valid_char = True
                elif (ord(c) == 32):
                    valid_char = True

                # Check if c is a valid character
                if (valid_char is False):
                    passed = False
                    break

            if (passed):
                validation_status = True

        return validation_status

    """Determine if a given description is valid"""
    @staticmethod
    def valid_description(description, title):
        return ((19 < len(description) < 2001)
                and (len(title) < len(description)))

    """Determine if a given price is valid"""
    @staticmethod
    def valid_price(price):
        return (10.00 <= price <= 10000.00)

    """Determine if a given last modification date is valid"""
    @staticmethod
    def valid_date(mod_date):
        min_date = datetime(2021, 1, 2)
        max_date = datetime(2025, 1, 2)
        return (min_date < mod_date < max_date)

    """Determine if a given owner is valid"""
    @staticmethod
    def valid_seller(owner):
        if (owner.email != ""):
            # Also need to check of owner is in database
            return True
        return False
