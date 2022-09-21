#review.py
from user import User

# comment this until Listing class implemented
#from listing import Listing

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
        self.id = None
        self.date_posted = None
        self.posting_user = None
        self.listing = None
        self.rating = None
        self.comment = None

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
    def data_posted(self, date):
        self._data_posted = date

    @property
    def posting_user(self):
        return self._posting_user

    @posting_user.setter
    def posting_user(self, user):
        if not isinstance(user, User):
            raise ValueError("posting user must be a User")
        self._posting_user = user

    @property
    def listing(self):
        return self._listing

    @listing.setter
    def listing(self, listing):

        # comment this until Listing class implemented
        #if not isinstance(listing, Listing):
        #    raise ValueError("listing must be a Listing")
        
        self._listing = listing

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, rating):
        if rating > 5:
            raise ValueError("rating must be out of 5 (stars)")
        self._rating = rating

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment
