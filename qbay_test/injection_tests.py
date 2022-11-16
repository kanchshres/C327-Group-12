import unittest
from qbay.user import User

class UnitTest(unittest.TestCase):

    def test_username():
        with open('./Generic_SQLI.txt') as f:
            for line in f:
                User.register(line, "testemail@gmail.com", "Password123!")

    def test_email():
        with open('./Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", line, "Password123!")

    def test_password():
        with open('./Generic_SQLI.txt') as f:
            for line in f:
                User.register("Bob", "testemail@gmail.com", line)
                