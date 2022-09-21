#review.py
from typing import TYPE_CHECKING
from user import User
from listing import Listing

class Review():
    """A review object that represents a review posted by a guest

    params:
    - id: the review id (unique), used to identify the review
    - date_posted: the date the review was posted
    - posting_user: the user that left the review
    - listing: the listing that the reviewing user stayed at/purchased
    - rating: the rating out of 5 stars the user left
    - comment: the comment the user left on the review

    Note: Checking that the user is a verified guest to the listing 
    has not been implemented yet
    """
    
    def __init__(self):
        self._id = None
        self._date_posted = None
        self._posting_user = None
        self._listing = None
        self._rating = None
        self._comment = None

    @property
    def __str__(self):
        return str(self._id)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def date_posted(self):
        return self._date_posted

    @date_posted.setter
    def date_posted(self, date):
        self._date_posted = date

    @property
    def posting_user(self):
        return self._posting_user

    @posting_user.setter
    def posting_user(self, user: User):
        self._posting_user = user

    @property
    def listing(self):
        return self._listing

    @listing.setter
    def listing(self, listing: Listing):
        self._listing = listing

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if not (0 < rating < 5):
            raise ValueError("rating must be out of 5 (stars)")
        self._rating = rating

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment

def test():
    review = Review()

    review.id = 1
    assert review.id == 1

    review.date_posted = "September 21, 2022"
    assert review.date_posted == "September 21, 2022"

    test_user = User()
    review.posting_user = test_user
    assert review.posting_user == test_user

    test_listing = Listing()
    review.listing = test_listing
    assert review.listing == test_listing

    review.rating = 3.4
    assert review.rating == 3.4

    review.comment = "hello world"
    assert review.comment == "hello world"

test()