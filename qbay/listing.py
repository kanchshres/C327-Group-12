# listing.py
from enum import Enum, unique
from user import User
from review import Review


class Listing:
    """Object representation of a digital Listing

	params:
    - title: Title of listing (string)
    - address: The location of the listing (string)
    - price: The cost of renting the listing (float)
    - seller: The User associated with the listing (User)
    - description: A short description (string)
    - reviews: A list of reviews associates with the listing (list[Review])
	"""
    def __init__(self):
        self._title = ""
        self._address = ""
        self._price = 0.0
        self._description = ""
        self._seller = User()
        self._reviews: list[Review] = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, subject):
        self._title = subject

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, location):
        self._address = location

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, text):
        self._description = text

    @property
    def seller(self):
        return self._seller

    @seller.setter
    def seller(self, person):
        self._seller = person

    @property
    def reviews(self) -> 'list[Review]':
        return self._reviews
    
    @reviews.setter
    def reviews(self, comments: 'list[Review]'):
        self._reviews = comments
    
    def add_review(self, review: 'Review'):
        self._reviews.append(review)