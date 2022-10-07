# listing.py
from enum import Enum, unique
from qbay.user import User
from qbay.review import Review
from datetime import date


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
    def __init__(self, title, description, price, mod_date, owner, 
                 address: str = ""):
        # Required
        self._title = title
        self._description = description
        self._price = price
        self._date = mod_date
        self._seller = owner

        # Extra
        self._address: str = address
        #self._reviews: list[Review] = []


    # Required
    """Fetches title of digital Listing"""
    @property
    def title(self):
        return self._title

    """Sets title for digital Listing"""
    @title.setter
    def title(self, title):
        if (valid_title(title)):
            self._title = title
            return True
        return False

    """Fetches description of digital Listing"""
    @property
    def description(self):
        return self._description

    """Sets title for digital Listing"""
    @description.setter
    def description(self, description, title):
        if (valid_description(description, title)):
            self._description = description
            return True
        return False

    """Fetches price of digital Listing"""
    @property
    def price(self):
        return self._price

    """Sets price for digital Listing"""
    @price.setter
    def price(self, price):
        if (valid_price(price)):
            self._price = price
            return True
        return False

    """Fetches last modification date of digital listing"""
    @property
    def date(self):
        return self._date

    """Updates last modification date of digital listing"""
    @date.setter
    def date(self, mod_date):
        if (valid_date(mod_date)):
            self._date = mod_date
            return True
        return False

    """Fetches owner of digital Listing"""
    @property
    def seller(self):
        return self._seller

    """Sets owner of digital Listing"""
    @seller.setter
    def seller(self, owner):
        if (valid_seller(owner)):
            self._seller = owner
            return True
        return False


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
    """
    @property
    def reviews(self) -> 'list[Review]':
        return self._reviews
    """
    
    """Sets reviews of Listing"""
    """
    @reviews.setter
    def reviews(self, comments: 'list[Review]'):
        self._reviews = comments
    """
    
    """Add reviews to listing"""
    """
    def add_review(self, review: 'Review'):
        self._reviews.append(review)
    """


"""Create a new listing - return true of succssfull and false otherwise"""
def create_listing(title, description, price, mod_date, owner):
    if (valid_title(title) and valid_description(description, title) and
        valid_price(price) and valid_date(mod_date) and
        valid_seller (owner)):
        listing = Listing(title, description, price, mod_date, owner)
        # Commit to database as well
        return True
    return False


"""Determine if a given title is valid """
def valid_title(title):
    validation_status = False

    # Validate title has maximum 80 characters and prefix/suffix of not 'space'
    if ((len(title) < 81) and (title[0] != ' ') and (title[-1] != ' ')):

        # Validate title only contains alphanumeric or 'space' characters
        passed = True
        for c in title:
            valid_char = False
            if ((47 < ord(c)) and (ord(c) < 58)):
                valid_char = True
            elif ((64 < ord(c)) and (ord(c) < 91)):
                valid_char = True
            elif ((96 < ord(c)) and (ord(c) < 123)):
                valid_char = True
            elif (ord(c) == 32):
                valid_char = True

            # Check if c is a valid character
            if (valid_char == False):
                passed = False
                break
        
        if (passed):
            validation_status = True

    return validation_status


"""Determine if a given description is valid"""
def valid_description(description, title):
    if ((19 < len(description)) and (len(description) < 2001)):
        if (len(title) < len(description)):
            return True
    return False


"""Determine if a given price is valid"""
def valid_price(price):
    if (10.00 <= price <= 10000.00):
        return True
    return False


"""Determine if a given last modification date is valid"""
def valid_date(mod_date):
    min_date = date(2021, 1, 2)
    max_date = date(2025, 1, 2)
    if (min_date < mod_date) and (mod_date < max_date):
        return True
    return False


"""Determine if a given owner is valid"""
def valid_seller(owner):
    if (owner.email != ""):
        # Also need to check of owner is in database
        return True
    return False


# Test Code
if (__name__ == "__main__"):
    # Testing Titles
    print("TESTING TITLES")
    t1 = ""
    i = 0
    while (i < 80):
        t1 = t1 + "a"
        i = i + 1
    t2 = " 4 bed 2 bath"
    t3 = "4 bed 2 bath "
    t4 = ""
    i = 0
    while (i < 81):
        t4 = t4 + "a"
        i = i + 1
    t5 = "4 bed 2 bath?"
    print(t1, valid_title(t1))
    print(t2, valid_title(t2))
    print(t3, valid_title(t3))
    print(t4, valid_title(t4))
    print(t5, valid_title(t5))
    print()
    # True, False, False, False, False

    # Testing Descriptions
    print("TESTING DESCRIPTIONS")
    t0 = "qwertyuiopqwertyui"
    des1 = ""
    i = 0
    while (i < 2000):
        des1 = des1 + "a"
        i = i + 1
    des2 = "qwertyuiopqwertyuiop"
    des3 = "qwertyuiopqwertyu"
    des4 = ""
    i = 0
    while (i < 2001):
        des4 = des4 + "a"
        i = i + 1
    print(des1, valid_description(des1, t0))
    print(des2, valid_description(des2, t0))
    print(des3, valid_description(des3, t0))
    print(des4, valid_description(des4, t0))
    print()
    # True, True, False, False

    # Testing Prices
    print("TESTING PRICES")
    p1 = 9.999999
    p2 = 10
    p3 = 10000
    p4 = 10000.001
    print(p1, valid_price(p1))
    print(p2, valid_price(p2))
    print(p3, valid_price(p3))
    print(p4, valid_price(p4))
    print()
    # False, True, True, False

    # Testing Dates
    print("TESING DATES")
    d1 = date(2021, 1, 2)
    d2 = date(2021, 1, 3)
    d3 = date(2025, 1, 1)
    d4 = date(2025, 1, 2)
    print(d1, valid_date(d1))
    print(d2, valid_date(d2))
    print(d3, valid_date(d3))
    print(d4, valid_date(d4))
    print()
    # False, True, True, False

    # Testing Ownership
    # Insert tests here