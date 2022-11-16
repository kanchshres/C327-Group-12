import unittest
from qbay.user import User

"""
This file defines the test cases for preventing SQL Injections
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
                