import unittest
from sqlalchemy import exc
from qbay.review import Review
from qbay.user import User
from qbay.listing import Listing
from datetime import datetime
from qbay.transaction import Transaction, TransactionStatus
from qbay.wallet import Wallet, BankingAccount


"""
This file defines the testing for implemented data models
"""


class UnitTest(unittest.TestCase):

    def test_user(self):
        user = User()

        user.username = "KanchShres"
        assert user.username == "KanchShres"

        user.email = "19ks62@queensu.ca"
        assert user.email == "19ks62@queensu.ca"

        user.password = "password123"
        assert user.password == "password123"

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
        """Sprint 2 Testing"""
        # Testing Titles
        t1 = ""
        i = 0
        while (i < 80):
            t1 = t1 + "a"
            i = i + 1
        t2 = " 4 bed 2 bath"
        t3 = "4 bed 2 bath "
        t4 = ""
        i = 0
        while (i < 81):
            t4 = t4 + "a"
            i = i + 1
        t5 = "4 bed 2 bath?"
        assert (Listing.valid_title(t1)) is True
        assert (Listing.valid_title(t2)) is False
        assert (Listing.valid_title(t3)) is False
        assert (Listing.valid_title(t4)) is False
        assert (Listing.valid_title(t5)) is False
        # True, False, False, False, False

        # Testing Descriptions
        t0 = "qwertyuiopqwertyui"
        des1 = ""
        i = 0
        while (i < 2000):
            des1 = des1 + "a"
            i = i + 1
        des2 = "qwertyuiopqwertyuiop"
        des3 = "qwertyuiopqwertyu"
        des4 = ""
        i = 0
        while (i < 2001):
            des4 = des4 + "a"
            i = i + 1

        assert (Listing.valid_description(des1, t0)) is True
        assert (Listing.valid_description(des2, t0)) is True
        assert (Listing.valid_description(des3, t0)) is False
        assert (Listing.valid_description(des4, t0)) is False
        # True, True, False, False

        # Testing Prices
        p1 = 9.999999
        p2 = 10
        p3 = 10000
        p4 = 10000.001
        assert (Listing.valid_price(p1)) is False
        assert (Listing.valid_price(p2)) is True
        assert (Listing.valid_price(p3)) is True
        assert (Listing.valid_price(p4)) is False
        # False, True, True, False

        # Testing Dates
        d1 = datetime(2021, 1, 2)
        d2 = datetime(2021, 1, 3)
        d3 = datetime(2025, 1, 1)
        d4 = datetime(2025, 1, 2)
        assert (Listing.valid_date(d1)) is False
        assert (Listing.valid_date(d2)) is True
        assert (Listing.valid_date(d3)) is True
        assert (Listing.valid_date(d4)) is False
        # False, True, True, False

        # Testing Ownership
        # Insert tests here
        """Sprint 2 Testing"""

    def test_user_database(self):
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

        assert User.register("u00", "test0@test.com", "Onetwo!") is True
        assert User.register("u01", "", "Onetwo!") is False
        assert User.register("u02", "test2@test.com", "") is False

    # need login function + database
    # def test_r1_2_user_register():
    #     """ Testing R1-2:
    #     User is uniquely identified by their user id.
    #     """

    #     user = login("test0@test.com", "Onetwo!")
    #     assert user is not None
    #     # might have to change later
    #     uuid_obj = UUID(user.id, version=4)
    #     assert str(uuid_obj) == user.id

    def test_r1_3_user_register(self):
        """ Testing R1-3:
        Email has to follow addr-spec defined in RFC 5322.
        """

        assert User.register("u01", "test.1@test.com", "Onetwo!") is True
        assert User.register("u02", "test2@test", "Onetwo!") is False
        assert User.register("u02", "test2@.com", "Onetwo!") is False
        assert User.register("u02", "@test.com", "Onetwo!") is False
        assert User.register("u02", "testing", "Onetwo!") is False
        assert User.register(
            "u02", "(Jon Test) test2@test.com", "Onetwo!") is False

    def test_r1_4_user_register(self):
        """ Testing R1-4:
        Password meets required complexity.
        """

        assert User.register("u02", "test2@test.com", "One23!") is True
        assert User.register("u03", "test3@test.com", "One2!") is False
        assert User.register("u03", "test3@test.com", "onetwo!") is False
        assert User.register("u03", "test3@test.com", "ONETWO!") is False
        assert User.register("u03", "test3@test.com", "Onetwo") is False

    def test_r1_5_user_register(self):
        """ Testing R1-5:
        User name is non-empty, alphanumeric-only, and spaces are allowed
        only if it is not as the prefix or suffix.
        """

        assert User.register("u03", "test3@test.com", "Onetwo!") is True
        assert User.register("User 04", "test4@test.com", "Onetwo!") is True
        assert User.register("", "test5@test.com", "Onetwo!") is False
        assert User.register("u05!", "test5@test.com", "Onetwo!") is False
        assert User.register("u05 ", "test5@test.com", "Onetwo!") is False
        assert User.register(" u05", "test5@test.com", "Onetwo!") is False

    def test_r1_6_user_register(self):
        """ Testing R1-6:
        User name length is longer 2 and less than 20 characters.
        """

        assert User.register("u05", "test5@test.com", "Onetwo!") is True
        assert User.register("u06ThisUsernameWork",
                             "test6@test.com", "Onetwo!") is True
        assert User.register("u07ThisUsernameWillNotWork",
                             "test7@test.com", "Onetwo!") is False
        assert User.register("u7", "test7@test.com", "Onetwo!") is False

# need database to check existing emails
# def test_r1_7_user_register():
#     """ Testing R1-7:
#     If email has been used, operation failed.
#     """

#     assert register("u07", "test7@test.com", "Onetwo!") is True
#     assert register("u08", "test7@test.com", "Onetwo!") is False

# need database for rest
# def test_r1_8_user_register():
#     """ Testing R1-8:
#     Billing Address is empty at time of registration.
#     """

#     user = login("u00", "test0@test.com", "Onetwo!")
#     assert user is not None
#     assert user.billing_address == ""

# def test_r1_9_user_register():
#     """ Testing R1-9:
#     Postal Code is empty at time of registration.
#     """

#     user = login("u00", "test0@test.com", "Onetwo!")
#     assert user is not None
#     assert user.postal_code == ""

# def test_r1_10_user_register():
#     """ Testing R1-10:
#     Balance should be initialized as 100 at time of registration.
#     """

#     user = login("u00", "test0@test.com", "Onetwo!")
#     assert user is not None
#     assert user.balance == 100


if __name__ == "__main__":
    unittest.main()
