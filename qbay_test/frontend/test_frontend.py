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
        # Email cannot be empty
        self.open(base_url + '/register')
        self.type("#username", "Test Two")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

        # Password cannot be empty
        self.type("#username", "Test Three")
        self.type("#email", "test01@test.com")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")

    def test_register_input(self, *_):
        """
        Testing R1-6:
        User name length is longer 2 and less than 20 characters.
        """
        # Input coverage testing by input partitioning
        # n = length of username
        # P1: n < 2
        self.open(base_url + '/register')
        self.type("#username", "4")
        self.type("#email", "test04@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P2: n > 20
        self.type("#username", "TestFiveUserNameIsTooLong")
        self.type("#email", "test05@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P3: n = 2
        self.type("#username", "u6")
        self.type("#email", "test06@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P4: n = 20
        self.type("#username", "Test Seven failure!!")
        self.type("#email", "test07@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#message")
        self.assert_text("Registration failed.", "#message")
        # P5: 2 < n < 20
        self.type("#username", "Test Eight")
        self.type("#email", "test08@test.com")
        self.type("#password", "Onetwo!")
        self.type("#password2", "Onetwo!")
        self.click('input[type="submit"]')
        self.assert_element("#welcome-header")
        self.assert_text("Please login below", "#welcome-header")

    def test_listing_update_fail(self, *_):
        """
        Testing R5-2:
        Price can only be increased.
        """
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
