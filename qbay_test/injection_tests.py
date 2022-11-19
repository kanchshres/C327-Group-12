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

    """Tests SQL Injection line on selected parameter"""
    def create_listing_helper(self, t, d, p, o, param):
        with open('./qbay_test/Generic_SQLI.txt') as f:
            i = 1
            for line in f:
                # Determine which parameter to substitute for injection line
                # Determine assertion statement based on parameter substituted
                if param == "title":
                    try:
                        t, d, p, o = line, d, p, o
                        Listing.create_listing(t, d, p, o)
                    except ValueError as e:
                        assert str(e) == "Invalid Title: " + line
                elif param == "description":
                    try:
                        t, d, p, o = "Place " + str(i), line, p, o
                        i += 1
                        Listing.create_listing(t, d, p, o)
                    except ValueError as e:
                        assert str(e) == "Invalid Description: " + line
                elif param == "price":
                    try: 
                        t, d, p, o = t, d, float(line), o
                        Listing.create_listing(t, d, p, o)
                    except ValueError as e:
                        # Check if error is of type 1 or type 2
                        if str(e) == "Invalid Price: " + str(p):
                            # Type 1: line is an invalid price
                            assert str(e) == "Invalid Price: " + str(p)
                        else:
                            # Type 2: line cannot be converted to float
                            assert (str(e)[0:33]) == ("could not convert " +
                                                      "string to float")
                            
    def test_create_listing_title_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the title parameter to test for vulnerabilities
        """
        username, email, password = "TestCL1", "testCL1@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        t, d, p = "", "This is a lovely place", 100
        self.create_listing_helper(t, d, p, account, "title")
    
    def test_create_listing_description_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the description parameter to test for vulnerabilities
        """
        username, email, password = "TestCL2", "testCL2@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        t, d, p = "Place x", "", 100
        self.create_listing_helper(t, d, p, account, "description")
    
    def test_create_listing_price_injection(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the price parameter to test for vulnerabilities
        """
        username, email, password = "TestCL3", "testCL3@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)
        t, d, p = "4 bed 2 bath", "This is a lovely place", 0
        self.create_listing_helper(t, d, p, account, "price")