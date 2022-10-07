import unittest

from qbay.review import Review
from qbay.user import User
from qbay.listing import Listing
from qbay.transaction import Transaction, TransactionStatus
from qbay.wallet import Wallet, BankingAccount


class UnitTest(unittest.TestCase):

    def test_user(self):
        user = User()

        user.id = 10
        assert user.id == 10

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

        review.date_posted = "September 21, 2022"
        assert review.date_posted == "September 21, 2022"

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
        """Sprint 1 Testing"""
        # Testing Initialization
        obj = Listing()
        # Testing param manipulation #
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
        """Sprint 1 Testing"""

        """Sprint 2 Testing"""
        # Testing Titles
        print("TESTING TITLES")
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
        print(t1, valid_title(t1))
        print(t2, valid_title(t2))
        print(t3, valid_title(t3))
        print(t4, valid_title(t4))
        print(t5, valid_title(t5))
        print()
        # True, False, False, False, False

        # Testing Descriptions
        print("TESTING DESCRIPTIONS")
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
        print(des1, valid_description(des1, t0))
        print(des2, valid_description(des2, t0))
        print(des3, valid_description(des3, t0))
        print(des4, valid_description(des4, t0))
        print()
        # True, True, False, False

        # Testing Prices
        print("TESTING PRICES")
        p1 = 9.999999
        p2 = 10
        p3 = 10000
        p4 = 10000.001
        print(p1, valid_price(p1))
        print(p2, valid_price(p2))
        print(p3, valid_price(p3))
        print(p4, valid_price(p4))
        print()
        # False, True, True, False

        # Testing Dates
        print("TESING DATES")
        d1 = date(2021, 1, 2)
        d2 = date(2021, 1, 3)
        d3 = date(2025, 1, 1)
        d4 = date(2025, 1, 2)
        print(d1, valid_date(d1))
        print(d2, valid_date(d2))
        print(d3, valid_date(d3))
        print(d4, valid_date(d4))
        print()
        # False, True, True, False

        # Testing Ownership
        # Insert tests here
        """Sprint 2 Testing"""


if __name__ == "__main__":
    unittest.main()
