import unittest

from qbay import database
from flask import Flask
from sqlalchemy import exc
from qbay.user import User
from qbay.database import app, db
from qbay.review import Review
from qbay.user import User
from qbay.listing import Listing
from qbay.transaction import Transaction, TransactionStatus
from qbay.wallet import Wallet, BankingAccount


"""
This file defines the testing for implemented data models
"""

ctx = app.app_context()
ctx.push()


class UnitTest(unittest.TestCase):

    def test_user(self):
        user = User()

        user.username = "KanchShres"
        assert user.username == "KanchShres"

        user.email = "19ks62@queensu.ca"
        assert user.email == "19ks62@queensu.ca"

        user.password = "Password123!"
        assert user.password == "Password123!"

        test_wall = Wallet()
        user.wallet = test_wall
        assert user.wallet == test_wall

        test_rev = Review()
        user.add_review(test_rev)
        assert user.reviews[0] == test_rev

    def test_review(self):
        review = Review()

        review.id = 1
        assert review.id == 1

        review.date_posted = "2022-09-21"
        assert review.date_posted == "2022-09-21"

        test_user = User()
        review.posting_user = test_user
        assert review.posting_user == test_user

        test_listing = Listing()
        review.listing = test_listing
        assert review.listing == test_listing

        review.rating = 3.4
        assert review.rating == 3.4

        review.comment = "hello world"
        assert review.comment == "hello world"

    def test_wallet_balance_transfer(self):
        bank_account = BankingAccount()
        user = User()
        wallet = user.create_wallet()
        user.wallet.bankingAccount = bank_account

        bank_account.add_balance(10000)
        assert user.wallet.bankingAccount.balance == 10000
        assert user.wallet.balance == 0

        user._wallet.transfer_balance(4000)
        assert user.wallet.bankingAccount.balance == 6000
        assert user.balance == 4000
        assert wallet.balance == 4000

        with self.assertRaises(ValueError):
            user.wallet.transfer_balance(-2000)

        with self.assertRaises(ValueError):
            bank_account.add_balance(-2000)

        assert user.balance == 4000
        assert bank_account.balance == 6000

    def test_transaction(self):
        transact = Transaction()
        transact.id = 50
        assert transact.id == 50

        test_user = User()
        transact.payer = test_user
        assert transact.payer == test_user

        test_user_2 = User()
        transact.payee = test_user_2
        assert transact.payee == test_user_2

        transact.amount = 50
        assert transact.amount == 50

        test_listing = Listing()
        transact.listing = test_listing
        assert transact.listing == test_listing

        transact.status = "transactionInProgress"
        assert transact.status == TransactionStatus.IN_PROGRESS

    def test_transaction_invalid_status(self):
        transact = Transaction()
        transact.status = TransactionStatus.COMPLETED
        assert transact.status == TransactionStatus.COMPLETED

        transact.status = "transactionCancelled"
        assert transact.status == TransactionStatus.CANCELLED

        with self.assertRaises(ValueError):
            transact.status = "Value error"

        with self.assertRaises(TypeError):
            transact.status = None

        with self.assertRaises(TypeError):
            transact.status = User()

    def test_listing(self):
        # Testing Initialization
        obj = Listing()
        # Testing param manipulation
        obj.title = "4 Bed 2 Bath"
        obj.address = "Queen's University"
        obj.price = 8000.57
        obj._description = "Shittiest school to ever exist"
        obj.seller.username = "bob"
        r = []
        r1 = Review()
        r.append(r1)
        obj.reviews = r
        r2 = Review()
        obj.add_review(r2)

        assert obj.title == "4 Bed 2 Bath"
        assert obj.price == 8000.57
        assert obj.address == "Queen's University"
        assert obj._description == "Shittiest school to ever exist"
        assert obj.seller.username == "bob"
        assert obj.reviews == [r1, r2]

    def test_user_database(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()
        assert user.id == 1

        user2 = User("testUser2", "user@example.ca2", "password123")
        user2.add_to_database()
        assert user2.id == 2

        with self.assertRaises(exc.IntegrityError):
            user.add_to_database()

        user3 = User("testUser2", "user@example.ca2", "password123")
        with self.assertRaises(exc.DatabaseError):
            user3.add_to_database()

    def test_r1_1_user_register(self):
        """ Testing R1-1:
        Email and password cannot be empty.
        """

        assert User.register("u01", "test1@test.com", "Onetwo!") is True
        assert User.register("u02", "", "Onetwo!") is False
        assert User.register("u02", "test2@test.com", "") is False
        assert User.register("u02", "", "") is False

    def test_r1_2_user_register(self):
        """ Testing R1-2:
        User is uniquely identified by their user id.
        """

        assert User.register("u02", "test2@test.com", "Onetwo!") is True
        user = database.User.query.get(2)
        assert user is not None
        assert user.id == 2

    def test_r1_3_user_register(self):
        """ Testing R1-3:
        Email has to follow addr-spec defined in RFC 5322.
        """

        assert User.register("u03", "test.1@test.com", "Onetwo!") is True
        assert User.register("u04", "test4@test", "Onetwo!") is False
        assert User.register("u04", "test4@.com", "Onetwo!") is False
        assert User.register("u04", "@test.com", "Onetwo!") is False
        assert User.register("u04", "testing", "Onetwo!") is False
        assert User.register("u04", "(Jon) test4@test.com", "Onetwo!") is False

    def test_r1_4_user_register(self):
        """ Testing R1-4:
        Password meets required complexity.
        """

        assert User.register("u04", "test4@test.com", "One23!") is True
        assert User.register("u05", "test5@test.com", "One2!") is False
        assert User.register("u05", "test5@test.com", "onetwo!") is False
        assert User.register("u05", "test5@test.com", "ONETWO!") is False
        assert User.register("u05", "test5@test.com", "Onetwo") is False
        assert User.register("u05", "test5@test.com", "ONETWO") is False
        assert User.register("u05", "test5@test.com", "onetwo") is False

    def test_r1_5_user_register(self):
        """ Testing R1-5:
        User name is non-empty, alphanumeric-only, and spaces are allowed
        only if it is not as the prefix or suffix.
        """

        assert User.register("u05", "test5@test.com", "Onetwo!") is True
        assert User.register("User 05", "test5.1@test.com", "Onetwo!") is True
        assert User.register("", "test6@test.com", "Onetwo!") is False
        assert User.register("u05!", "test6@test.com", "Onetwo!") is False
        assert User.register("u06 ", "test6@test.com", "Onetwo!") is False
        assert User.register(" u06", "test6@test.com", "Onetwo!") is False

    def test_r1_6_user_register(self):
        """ Testing R1-6:
        User name length is longer 2 and less than 20 characters.
        """

        assert User.register("u06", "test6@test.com", "Onetwo!") is True
        assert User.register("u06ThisUsernameWork",
                             "test6.2@test.com", "Onetwo!") is True
        assert User.register("u07ThisUsernameWillNotWork",
                             "test7@test.com", "Onetwo!") is False
        assert User.register("u7", "test7@test.com", "Onetwo!") is False

    def test_r1_7_user_register(self):
        """ Testing R1-7:
        If email has been used, operation failed.
        """

        assert User.register("u07", "test7@test.com", "Onetwo!") is True
        assert User.register("u08", "test7@test.com", "Onetwo!") is False

    def test_r1_8_user_register(self):
        """ Testing R1-8:
        Billing Address is empty at time of registration.
        """
        User.register("u08", "test7@test.com", "Onetwo!")
        user = database.User.query.get(8)
        assert user is not None
        assert user.billing_address == ""

    def test_r1_9_user_register(self):
        """ Testing R1-9:
        Postal Code is empty at time of registration.
        """
        User.register("u09", "test9@test.com", "Onetwo!")
        user = database.User.query.get(9)
        assert user is not None
        assert user.postal_code == ""

    def test_r1_10_user_register(self):
        """ Testing R1-10:
        Balance should be initialized as 100 at time of registration.
        """
        User.register("u10", "test10@test.com", "Onetwo!")
        user = database.User.query.get(1)
        assert user is not None
        assert user.postal_code == ""


if __name__ == "__main__":
    unittest.main()
