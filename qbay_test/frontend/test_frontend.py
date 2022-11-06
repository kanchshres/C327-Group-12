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

    