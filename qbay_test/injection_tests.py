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
        account = User.login(email, password)
        return account

    def create_listing_helper(self, t, d, p, o, param):
        # Tests SQL Injection line on selected parameter
        with open('./qbay_test/Generic_SQLI.txt') as f:
            i = 1
            for line in f:
                # Determine which parameter to substitute for injection line
                # Determine assertion statement based on parameter substituted
                if param == "title":
                    try:
                        t, d, p, o = line, d, p, o
                        Listing.create_listing(t, d, p, o)
                        assert (Listing.valid_title(line)) is True
                    except ValueError as e:
                        assert (Listing.valid_title(line)) is False
                elif param == "description":
                    try:
                        t, d, p, o = "Place " + str(i), line, p, o
                        i += 1
                        Listing.create_listing(t, d, p, o)
                        assert (Listing.valid_description(line, t)) is True
                    except ValueError as e:
                        assert (Listing.valid_description(line, t)) is False
                elif param == "price":
                    try: 
                        t, d, p, o = t, d, float(line), o
                        Listing.create_listing(t, d, p, o)
                        assert (Listing.valid_price(line)) is True
                    except ValueError as e:
                        # Could not convert string to float
                        pass
                
    def test_creat_listing_title(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the title parameter to test for vulnerabilities
        """
        username, email, password = "TestCL1", "testCL1@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "", "This is a lovely place", 100
        owner, parameter = account, "title"
        self.create_listing_helper(title, description, price, owner, parameter)
    
    def test_create_listing_description(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the description parameter to test for vulnerabilities
        """
        username, email, password = "TestCL2", "testCL2@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "Place x", "", 100
        owner, parameter = account, "description"
        self.create_listing_helper(title, description, price, owner, parameter)
    
    def test_create_listing_price(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the price parameter to test for vulnerabilities
        """
        username, email, password = "TestCL3", "testCL3@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        title, description, price = "4 bed 2 bath", "This is a lovely place", 0
        owner, parameter = account, "price"
        self.create_listing_helper(title, description, price, owner, parameter)