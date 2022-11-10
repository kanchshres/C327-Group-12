from seleniumbase import BaseCase
from qbay_test.conftest import base_url
from unittest.mock import patch
from qbay.user import User

"""
This file defines all integration tests for the frontend registration page.
"""


class FrontEndTests(BaseCase):
    def test_register_success(self, *_):
        # Output coverage testing
        # Output: User is registered and in the database
        self.open(base_url + '/register')
        self.type("#email", "test01@test.com")
        self.type("#username", "Test One")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')

        self.type("#email", "test01@test.com")
        self.type("#password", "Onetwo!")
        self.click('input[type="submit"]')

        self.assert_element("#welcome-header")
        self.assert_text("Welcome Test One!", "#welcome-header")

    def test_register_fail(self, *_):
        """
        Testing R1-1:
        Email and password cannot be empty.
        """
        # Functionality Testing by Requirement Partitioning
        # R1T1: Both empty
        self.open(base_url + '/register')
        self.type("#username", "Test Two")
        self.type("#email", "")
        self.type("#password", "")
        self.type("#password2", "")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # R1T2: Email empty, password not
        self.open(base_url + '/register')
        self.type("#username", "Test Three")
        self.type("#email", "")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # R1T3: Email not empty, password empty
        self.type("#username", "Test Four")
        self.type("#email", "test04@test.com")
        self.type("#password", "")
        self.type("#password2", "")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # R1T4: Email not empty, password not empty
        self.type("#username", "Test Five")
        self.type("#email", "test05@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Please login below", "#welcome-header")

    def test_register_input(self, *_):
        """
        Testing R1-6:
        User name length is longer 2 and less than 20 characters.
        """
        # Input coverage testing by input partitioning
        # n = length of username
        # P1: n < 2
        self.open(base_url + '/register')
        self.type("#username", "6")
        self.type("#email", "test06@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P2: n > 20
        self.type("#username", "TestSevenUserNameIsTooLong")
        self.type("#email", "test07@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P3: n = 2
        self.type("#username", "u8")
        self.type("#email", "test08@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P4: n = 20
        self.type("#username", "Test Nine failure!!")
        self.type("#email", "test09@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P5: 2 < n < 20
        self.type("#username", "Test Ten")
        self.type("#email", "test10@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Please login below", "#welcome-header")

    def test_listing_update_fail(self, *_):
        # Input coverage testing by Input Partitioning

        # Price decreased.
        self.open(base_url + '/register')
        self.type("#email", "updatelisting01@test.com")
        self.type("#username", "Listing Update 01")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')

        self.open(base_url + '/login')
        self.type("#email", "updatelisting01@test.com")
        self.type("#password", "Onetwo!")
        self.click('input[type="submit"]')

        self.click_link("Create Listing")
        self.type("#title", "4 bed 2 bath")
        self.type("#description", "This is a lovely place with 4 beds 2 bath")
        self.type("#price", 100)
        self.click('input[type="submit"]')

        self.click_link("Update Your Listings")
        self.click('input[type="radio"]')
        self.click('input[type="submit"]')
        
        self.type("#price", 49.99)
        self.click('input[type="submit"]')
        self.assert_element("#messages")
        self.assert_text("Invalid Price: 49.99", "#messages")

        # Price increased
        self.type("#price", 149.99)
        self.click('input[type="submit"]')
        self.assert_element("#messages")
        self.assert_text("Price updated successfully: 149.99", "#messages")

    def test_listing_update_success(self, *_):
        # Output coverage testing

        # Outputs newly updated listing
        self.open(base_url + '/register')
        self.type("#email", "updatelisting02@test.com")
        self.type("#username", "Listing Update 02")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')

        self.open(base_url + '/login')
        self.type("#email", "updatelisting02@test.com")
        self.type("#password", "Onetwo!")
        self.click('input[type="submit"]')

        self.click_link("Create Listing")
        self.type("#title", "5 bed 3 bath")
        self.type("#description", "This is a lovely place with 5 beds 3 bath")
        self.type("#price", 499.99)
        self.click('input[type="submit"]')

        self.click_link("Update Your Listings")
        self.click('input[type="radio"]')
        self.click('input[type="submit"]')
        
        self.type("#description", "This is a comfy place with 5 beds 3 bath")
        self.click('input[type="submit"]')
        self.assert_element("#messages")
        self.assert_text("Description updated successfully: " +
                         "This is a comfy place with 5 beds 3 bath", 
                         "#messages")

    def test_listing_update_requirement(self, *_):
        """ Requirement Partitioning """
        # Register & Log-in
        email, username = "createlisting03@test.com", "Create Listing 03"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Create listing
        t, d, p = "6 Bed 3 Bath", "This is a lovely place", 10
        self.create_listing_helper(t, d, p)

        # R5-2 : Price can only be increased but cannot be decreased
        # R5-2P: price1 < price2
        t, d, p = t, d, 11.00
        self.update_listing_helper(t, d, p)
        self.assert_element("#messages")
        self.assert_text("Price updated successfully: 11.00", "#messages")
        self.open(base_url)

        # R5-2N: price2 < price 1
        t, d, p = t, d, 10
        self.update_listing_helper(t, d, p)
        self.assert_element("#messages")
        self.assert_text("Invalid Price: 10.0", "#messages")
        self.open(base_url)

        # R5-3 : last_modified_date should be updated when the update operation
        #        is successful
        # R5-3P: 

        # R5-3N: 

        # R5-4 : When updating an attribute, it must follow the same 
        #        requirements as when it were created
        # R5-4P: 20 <= price1 < price2 <= 10000
        t, d, p = t, d, 12.00
        self.update_listing_helper(t, d, p)
        self.assert_element("#messages")
        self.assert_text("Price updated successfully: 12.00", "#messages")
        self.open(base_url)

        # R5-4N: 20 <= price1 <= 10000 < price2
        t, d, p = t, d, 69420
        self.update_listing_helper(t, d, p)
        self.assert_element("#messages")
        self.assert_text("Invalid Price: 69420.0", "#messages")
        
    def resgister_helper(self, email, username, password):
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

    def update_listing_helper(self, title, description, price):
        # Update listing given title, description, price
        self.click_link("Update Your Listings")
        self.click('input[type="radio"]')
        self.click('input[type="submit"]')
        self.type("#title", title)
        self.type("#description", description)
        self.type("#price", price)
        self.click('input[type="submit"]')
