#listing.py
from enum import Enum, unique
from user import User

class Listing:
	"""
	Object representation of a digital Listing

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
		self._seller = None # Seller should be of type User
		#self._reviews: list[Review] = []

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


    # Missing Review object
	"""
    @property
	def reviews(self) -> list[Review]
		return self._reviews


	@reviews.setter
	def reviews(self, comments:list[Review]):
		if all(isinstance(i, list[Review]) for i in comments):
			self._reviews = comments
		else:
			raise ValueError("comments must be a list of Review objects")


	#def add_review(self, review:Review):
		if not isinstance(review, Review):
			raise ValueError("review must be a Review object")
		self._reviews.append(review)
    """


# Test Code #
if (__name__ == "__main__"):
    # Testing Initialization
    obj = Listing()
    print("Listing Info")
    print("title: " + obj.title)
    print("address: " + obj.address)
    print("price: ", end = "")
    print(obj.price)
    print("description: " + obj.description)
    print("Seller: ", end = "")
    print(obj.seller)

    
    # Testing param maniupulation #
    obj.title = "4 Bed 2 Bath"
    obj.address = "Queen's University"
    obj.price = 8000.57
    obj._description = "Shittiest school to ever exist"
    # bob = User()
    obj.seller = "Bob" # Should be an object of type User

    print("")
    print("Listing Info")
    print("title: " + obj.title)
    print("address: " + obj.address)
    print("price: $", end = "")
    print(obj.price)
    print("description: " + obj.description)
    print("Seller: ", end = "")
    print(obj.seller)