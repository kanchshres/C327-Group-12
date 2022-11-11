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

    def test_listing_update_requirement(self, *_):
        """ Requirement Partitioning """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "updatelisting01@test.com", "Update Listing 01"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Create listing
        t, d, p = "6 Bed 3 Bath", "This is a lovely place", 10
        self.create_listing_helper(t, d, p)

        # R5-2 : Price can only be increased but cannot be decreased
        # R5-2P: price1 < price2
        t, d, p = t, d, 11.00
        element, text = "#messages", "Price updated successfully: 11.00"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R5-2N: price2 < price 1
        t, d, p = t, d, 10
        element, text = "#messages", "Invalid Price: 10.0"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R5-3 : last_modified_date should be updated when the update operation
        #        is successful
        element, text = "#listing", datetime.now().date().isoformat()
        self.assert_helper(element, text, None)

        # R5-4 : When updating an attribute, it must follow the same 
        #        requirements as when it were created
        # R5-4P: 20 <= price1 < price2 <= 10000
        t, d, p = t, d, 12.00
        element, text = "#messages", "Price updated successfully: 12.00"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R5-4N: 20 <= price1 <= 10000 < price2
        t, d, p = t, d, 69420
        element, text = "#messages", "Invalid Price: 69420.0"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

    def test_listing_update_input(self, *_):
        """ Input Partitioning """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "updatelisting02@test.com", "Listing Update 02"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Create Listing
        t, d, p = "4 bed 2 bath", "This is a lovely place", 100
        self.create_listing_helper(t, d, p)

        # Price decreased.
        t, d, p = t, d, 49.99
        element, text = "#messages", "Invalid Price: 49.99"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Price increased
        t, d, p = t, d, 149.99
        element, text = "#messages", "Price updated successfully: 149.99"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

    def test_listing_update_output(self, *_):
        """ Output Coverage"""
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "updatelisting03@test.com", "Listing Update 03"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Create Listing
        t, d, p = "5 bed 3 bath", "This is a lovely place", 499.99
        self.create_listing_helper(t, d, p)

        # Outputs newly updated listing
        # Sucessfull Update 
        t, d, p = t, "This is a very lovely place", p
        element = "#messages"
        text = "Description updated successfully: This is a very lovely place"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Failure due to invalid title
        t, d, p = "5 bed 3 bath!", d, p
        element, text = "#messages", "Invalid Title"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Failure due to invalid description
        t, d, p = "5 bed 3 bath", "Good place", p
        element, text = "#messages", "Invalid Description"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Failure due to invalid price
        t, d, p = t, "This is a very lovely place", 69.99
        element, text = "#messages", "Invalid Price"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

    def test_login_output_coverage(self, *_):
        """ Test login page using output coverage (exhaustive) testing 
        method.
        """
        # clear database
        with app.app_context():
            db.drop_all()
            db.create_all()

        # Output: User successfullly logs in in with correct login info
        self.open(base_url + '/register')
        self.type("#email", "bob@gmail.com")
        self.type("#username", "Bob")
        self.type("#password", "Password123!")
        self.type("#password2", "Password123!")
        self.click('input[type="submit"]')

        self.type("#email", "bob@gmail.com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')

        self.assert_element("#welcome-header")
        self.assert_text("Welcome Bob!", "#welcome-header")

        # Output: User inputs invalid email or password such that they 
        # do not meet the requirements of a valid email and/or a valid 
        # password (Won't even check database).
        self.open(base_url + '/login')

        self.type("#email", "b.o.b.@gmail..com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Invalid email or password", "#message")

        # Output: Email and/or password is incorrect, that is, the 
        # email and password do not match any entry in the database.
        self.type("#email", "notindatabase@gmail.com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Incorrect email or password", "#message")

    def test_login_input_coverage(self, *_):
        """ Test login page using input coverage (input partitioning) 
        testing method.
        """
        # Partition 1: Correct input
        self.open(base_url + '/register')
        self.type("#email", "bob@gmail.com")
        self.type("#username", "Bob")
        self.type("#password", "Password123!")
        self.type("#password2", "Password123!")
        self.click('input[type="submit"]')

        self.type("#email", "bob@gmail.com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')

        self.assert_element("#welcome-header")
        self.assert_text("Welcome Bob!", "#welcome-header")

        # Partition 2: Invalid email
        self.open(base_url + '/login')
        self.type("#email", "")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Invalid email or password", "#message")

        # Partition 3: Invalid password
        self.type("#email", "bob@gmail.com")
        self.type("#password", "")
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Invalid email or password", "#message")

        # Partition 4: Invalid email and password
        self.type("#email", "")
        self.type("#password", "")
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Invalid email or password", "#message")

    def test_login_req_coverage(self, *_):
        """Test login page using the requirement partitioning testing 
        method
        """
        # clear database
        with app.app_context():
            db.drop_all()
            db.create_all()

        # R2-1: A user can log in using her/his email address and the 
        # password.
        self.open(base_url + '/register')
        self.type("#email", "bob@gmail.com")
        self.type("#username", "Bob")
        self.type("#password", "Password123!")
        self.type("#password2", "Password123!")
        self.click('input[type="submit"]')

        self.type("#email", "bob@gmail.com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')

        self.assert_element("#welcome-header")
        self.assert_text("Welcome Bob!", "#welcome-header")

        # R2-2: Shouldn't even check database if email or password is 
        # not valid.
        self.open(base_url + '/login')
        self.type("#email", "b.o.b.@gmail.com")
        self.type("#password", "psw")
        self.click('input[type="submit"]')

        self.assert_element("#message")
        self.assert_text("Invalid email or password", "#message")

