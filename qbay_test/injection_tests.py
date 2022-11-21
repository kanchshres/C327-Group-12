import unittest
from qbay.database import app, db
from qbay.user import User
from qbay.listing import Listing
from datetime import datetime

"""
This file defines all SQL Injection Back-end Tests
"""


class UnitTest(unittest.TestCase):
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
