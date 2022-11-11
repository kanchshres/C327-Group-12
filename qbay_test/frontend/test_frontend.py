from seleniumbase import BaseCase
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.user import User
from qbay.database import app, db
from datetime import datetime

"""
This file defines all integration tests for the frontend registration page.
"""


class FrontEndTests(BaseCase):
    def initialize_database(self):
        # Clear database
        with app.app_context():
            db.drop_all()
            db.create_all()
    
    def register_helper(self, email, username, password):
        # Register user given email, username, password
        self.open(base_url + '/register')
        self.type("#email", email)
        self.type("#username", username)
        self.type("#password", password)
        self.type("#password2", password)
        self.click('input[type="submit"]')

    def login_helper(self, email, password):
        # Log-in given email, password
        self.open(base_url + '/login')
        self.type("#email", email)
        self.type("#password", password)
        self.click('input[type="submit"]')
    
    def create_listing_helper(self, title, description, price):
        # Create listing given title, description, price
        self.click_link("Create Listing")
        self.type("#title", title)
        self.type("#description", description)
        self.type("#price", price)
        self.click('input[type="submit"]')

    def update_listing_helper(self, title, description, price):
        # Update listing given title, description, price
        self.click_link("Update Your Listings")
        self.click('input[type="radio"]')
        self.click('input[type="submit"]')
        self.type("#title", title)
        self.type("#description", description)
        self.type("#price", price)
        self.click('input[type="submit"]')

    def assert_helper(self, element, text, url):
        # Assert given an element, text, and return to desired url
        self.assert_element(element)
        self.assert_text(text, element)
        if (url):
            self.open(url)
    
    def test_create_listing_requirement(self, *_):
        """ Requirement Partitioning """
        # Initialize database
        self.initialize_database()
        
        # Register & Log-in
        email, username = "createlisting01@test.com", "Create Listing 01"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # R4-1 : The title of the product has to be alphanumeric-only, and
        #        space allowed only if it is not as prefix and suffix
        # R4-1P: 1 Bed 1 Bath
        t, d, p = "1 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

        # R4-1N: 1 Bath 1 Bath!
        t, d, p = "1 Bed 1 Bath!", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 1 Bed 1 Bath!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R4-2 : The title of the product is no longer than 80 characters
        # R4-2P: len(title) <= 80
        t, d, p = "2 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

        # R4-2N: 80 < len(title)
        t, d, p = "a" * 81, "This is a lovely place", 100
        element, text = "#message", "Invalid Title: " + t
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R4-3 : The description of the product can be arbitrary characters, 
        #        with a minimum character length of 20 and a maximum of 2000
        # R4-3P: 20 <= len(description) <= 2000
        t, d, p = "3 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

        # R4-3N: len(description) < 20 < 2000
        t, d, p = "3 Bed 1 Baths", "lol", "100"
        element, text = "#message", "Invalid Description: lol"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)
        
        # R4-4 : Description has to be longer than product's title
        # R4-4P: len(title) < len(description)
        t, d, p = "4 Bed 1 Baths", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

        # R4-4N: len(description) < len(title)
        t, d, p = "This is the listing A", "This is a lovely see", 100
        self.create_listing_helper(t, d, p)
        element, text = "#message", "Invalid Description: " + d
        self.assert_helper(element, text, base_url)

        # R4-5 : Price has to be of range [10, 10000]
        # R4-5P: 10 <= price <= 10000
        t, d, p = "5 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

        # R4-5N: 10 < 10000 < price
        t, d, p = "5 Bed 1 Baths", "This is a lovely place", 69420
        element, text = "#message", "Invalid Price: 69420.0"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)
        
        # R4-8 : A user cannot create products that have the same title
        # R4-8P: title1 != title2
        t, d, p = "6 Bed 1 Bath", "This is a lovely place", 100
        self.create_listing_helper(t, d, p)
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.assert_helper(element, text, None)
        
        # R4-8N: title1 == title2
        t, d, p = "1 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 1 Bed 1 Bath"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

    def test_create_listing_input(self, *_):
        """ Input Paritioning """
        # Initialize database
        self.initialize_database()
        
        # Register & Log-in
        email, username = "createlisting02@test.com", "Create Listing 02"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Title: Valid   | Description: Valid   | Price: Valid
        t, d, p = "1 Bed 4 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 02!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

        # Title: Valid   | Description: Valid   | Price: Invalid
        t, d, p = "1 Bed 4 Baths", "This is a lovely place", 1
        element, text = "#message", "Invalid Price: 1.0"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Title: Valid   | Description: Invalid | Price: Valid
        t, d, p = "1 Bed 4 Baths", "lol", 100
        element, text = "#message", "Invalid Description: lol"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Title: Invalid | Description: Valid   | Price: Valid
        t, d, p = "1 Bed 4 Bath!", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Title: Valid   | Description: Invalid | Price: Invalid
        t, d, p = "1 Bed 4 Baths", "lol", 1
        element, text = "#message", "Invalid Price: 1.0"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)
        
        # Title: Invalid   | Description: Invalid | Price: Valid
        t, d, p = "1 Bed 4 Bath!", "lol", 100
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)
        
        # Title: Invalid | Description: Valid   | Price: Invalid
        t, d, p = "1 Bed 4 Bath!", "This is a lovely place", 1
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Title: Invalid | Description: Invalid | Price: Invalid
        t, d, p = "1 Bed 4 Bath!", "lol", 1
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url) 

    def test_create_listing_output(self, *_):
        """ Output Coverage """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, password = "createlisting03@test.com", "Onetwo!"
        username = "Create Listing 03"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Successful Creation
        t, d, p = "5 Bed 3 Bath", "This is a lovely place", 100
        self.create_listing_helper(t, d, p)
        element, text = "#welcome-header", "Welcome Create Listing 03!"
        self.assert_helper(element, text, None)

        # Invalid Title
        t, d, p = "5 Bed 3 Bath!", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 5 Bed 3 Bath!"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Invalid Description
        t, d, p = "5 Bed 3 Baths", "lol", 100
        element, text = "#message", "Invalid Description: lol"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Invalid Price
        t, d, p = "5 Bed 3 Baths", "This is a lovely place", 1
        element, text = "#message", "Invalid Price: 1.0"
        self.create_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)
