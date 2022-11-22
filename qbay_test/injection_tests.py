import unittest
from qbay.database import app, db
from qbay.user import User
from qbay.listing import Listing
from datetime import datetime

"""
This file defines all SQL Injection Back-end Tests
"""


class UnitTest(unittest.TestCase):
    def test_username(self):
        """ For each line/input/test-case, pass through the 
        User.register() function as the username parameter to test for 
        vulnerabilities to SQL Injection
        """
        with open("./qbay_test/Generic_SQLI.txt") as f:
            for line in f:
                User.register(line, "testemail@gmail.com",
                              "Password123!")

    def test_email(self):
        """ For each line/input/test-case, pass through the 
        User.register() function as the email parameter to test for 
        vulnerabilities to SQL Injection
        """
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", line, "Password123!")

    def test_password(self):
        """ For each line/input/test-case, pass through the 
        User.register() function as the password parameter to test for 
        vulnerabilities to SQL Injection
        """
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", "testemail@gmail.com", line)

    """Create account to verify in test_create_listing functions"""

    def create_account(self, username, email, password):
        # Create account
        User.register(username, email, password)
        return User.login(email, password)

    def test_create_listing_title_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the title parameter to test for vulnerabilities
        """
        username, email, password = "TestCL1", "testCL1@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "", "This is a lovely place", 100
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                try:
                    # Parameter changed
                    title = line
                    Listing.create_listing(title, description, price, account)
                except ValueError as e:
                    assert str(e) == "Invalid Title: " + line

    def test_create_listing_description_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the description parameter to test for vulnerabilities
        """
        username, email, password = "TestCL2", "testCL2@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "Place x", "", 100
        with open('./qbay_test/Generic_SQLI.txt') as f:
            i = 1
            for line in f:
                try:
                    # Parameters changed
                    title, description, i = "Place " + str(i), line, i + 1
                    Listing.create_listing(title, description, price, account)
                except ValueError as e:
                    assert str(e) == "Invalid Description: " + line

    def test_create_listing_price_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the price parameter to test for vulnerabilities
        """
        username, email, password = "TestCL3", "testCL3@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "4 bed 2 bath", "This is a lovely place", 0
        with open('./qbay_test/Generic_SQLI.txt') as f:
            for line in f:
                try:
                    # Parameter changed
                    price = float(line)
                    Listing.create_listing(title, description, price, account)
                except ValueError as e:
                    # Check if error is of type 1 or type 2
                    try:
                        # Type 1: line cannot be converted to float
                        assert (str(e)[0:33]) == ("could not convert " +
                                                  "string to float")
                    except AssertionError:
                        # Type 2: line is an invalid price
                        assert str(e) == "Invalid Price: " + str(price)

    def test_listing_inject_seller(self):
        """
        Attemp to pass in the injection text as plain string to the database
        Should catch attribute error when trying to parse the object
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        with open("./qbay_test/Generic_SQLI.txt") as f:
            cur = 0
            for line in f:
                title = f"Testing title {cur}"
                try:
                    Listing.create_listing(title=title,
                                           description="testing description 1",
                                           price=10.0,
                                           owner=line,
                                           address="101 Kingstreet"
                                           )
                except AttributeError as e:
                    # AttributeError e should prints "Invalid attribute: id"
                    # e.name should be the same as the invalid attribute name"
                    assert e.name == 'id'
                cur += 1

    def test_listing_inject_address(self):
        """
        Pass in injection string into database.
        String should be accepted but does not execute code
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()

        with open("./qbay_test/Generic_SQLI.txt") as f:
            cur = 0
            for line in f:
                title = f"Testing title {cur}"
                Listing.create_listing(title=title,
                                       description="testing description 1",
                                       price=10.0,
                                       owner=user,
                                       address=line
                                       )
                cur += 1
