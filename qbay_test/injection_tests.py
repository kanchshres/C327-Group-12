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
        
    def test_creat_listing_title(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the title parameter to test for vulnerabilities
        """
        username, email, password = "TestCL1", "testCL1@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)

        with open('./qbay_test/Generic_SQLI.txt') as f:
            t, d, p, o = "", "This is a lovely place", 100.00, account
            for line in f:
                t, d, p, o = line, d, p, o
                try: 
                    Listing.create_listing(t, d, p, o)
                    raise ValueError(f"SECURITY BREACHED: {line}")
                except (ValueError):
                    self.assertRaises(ValueError)
    
    def test_create_listing_description(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the description parameter to test for vulnerabilities
        """
        username, email, password = "TestCL2", "testCL2@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)

        with open('./qbay_test/Generic_SQLI.txt') as f:
            t, d, p, o = "69 Ligma Road", "", 100.00, account
            for line in f:
                t, d, p, o = t, line, p, o
                try: 
                    Listing.create_listing(t, d, p, o)
                    raise ValueError(f"SECURITY BREACHED: {line}")
                except (ValueError):
                    self.assertRaises(ValueError)
    
    def test_create_listing_price(self):
        """
        For each line/input/test-case, pass through the Listing.create_listing
        function as the price parameter to test for vulnerabilities
        """
        username, email, password = "TestCL3", "testCL3@gmail.com", "Onetwo!"
        account = self.create_account(username, email, password)

        with open('./qbay_test/Generic_SQLI.txt') as f:
            t, d, p, o = "69 Ligma Road", "This is a lovely place", "", account
            for line in f:
                t, d, p, o = t, d, line, o
                try: 
                    Listing.create_listing(t, d, p, o)
                    raise ValueError(f"SECURITY BREACHED: {line}")
                except (ValueError):
                    self.assertRaises(ValueError)