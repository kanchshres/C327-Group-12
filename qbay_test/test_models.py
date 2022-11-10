import unittest

from qbay import database
from flask import Flask
from sqlalchemy import exc
from qbay.user import User
from qbay.database import app, db
from qbay.review import Review
from qbay.listing import Listing
from datetime import datetime
from qbay.transaction import Transaction, TransactionStatus
from qbay.wallet import Wallet, BankingAccount
from datetime import datetime, timedelta
import pytest


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
        user.wallet.bankingAccount = bank_account

        assert user.wallet.bankingAccount.balance == 0
        assert user.wallet.balance == 100

        bank_account.add_balance(10000)
        assert user.wallet.bankingAccount.balance == 10000
        assert user.wallet.balance == 100

        user._wallet.transfer_balance(4000)
        assert user.wallet.bankingAccount.balance == 6000
        assert user.balance == 4100
        assert user.wallet.balance == 4100

        with self.assertRaises(ValueError):
            user.wallet.transfer_balance(-2000)

        with self.assertRaises(ValueError):
            bank_account.add_balance(-2000)

        assert user.balance == 4100
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
        # Testing param manipulation
        obj.title = "4 Bed 2 Bath"
        obj.address = "Queen's University"
        obj.price = 10
        obj._description = "Shittiest school to ever exist"
        obj.seller.username = "bob"
        r = []
        r1 = Review()
        r.append(r1)
        obj.reviews = r
        r2 = Review()
        obj.add_review(r2)

        assert obj.title == "4 Bed 2 Bath"
        assert obj.price == 10
        assert obj.address == "Queen's University"
        assert obj._description == "Shittiest school to ever exist"
        assert obj.seller.username == "bob"
        assert obj.reviews == [r1, r2]
        """Sprint 1 Testing"""

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

        assert user.add_to_database() is False

        user3 = User("testUser2", "user@example.ca2", "password123")
        assert user3.add_to_database() is False

    def test_user_query(self):
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()

        assert database.User.query.get(user.id).username == user.username
        assert database.User.query.get(user.id).email == user.email
        assert database.User.query.get(user.id).password == user.password

    def test_r1_1_user_register(self):
        """ Testing R1-1:
        Email and password cannot be empty.
        """
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        assert User.register("u01", "test1@test.com", "Onetwo!") is True
        assert User.register("u02", "", "Onetwo!") is False
        assert User.register("u02", "test2@test.com", "") is False
        assert User.register("u02", "", "") is False

    def test_r1_2_user_register(self):
        """ Testing R1-2:
        User is uniquely identified by their user id.
        """
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        assert User.register("u01", "test2.1@test.com", "Onetwo!") is True
        user = database.User.query.get(1)
        assert user is not None
        assert user.id == 1

        assert User.register("u02", "test2.2@test.com", "Onetwo!") is True
        user2 = database.User.query.get(2)
        assert user2 is not None
        assert user2.id == 2

    def test_r1_3_user_register(self):
        """ Testing R1-3:
        Email has to follow addr-spec defined in RFC 5322.
        """
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

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
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()
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
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

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
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        assert User.register("u05", "test5@test.com", "Onetwo!") is True
        assert User.register("u06ThisUsernameWork",
                             "test6@test.com", "Onetwo!") is True
        assert User.register("u07ThisUsernameWillNotWork",
                             "test7@test.com", "Onetwo!") is False
        assert User.register("u7", "test7@test.com", "Onetwo!") is False

    def test_r1_7_user_register(self):
        """ Testing R1-7:
        If email has been used, operation failed.
        """
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        assert User.register("u07", "test7@test.com", "Onetwo!") is True
        assert User.register("u08", "test7@test.com", "Onetwo!") is False

    def test_r1_8_user_register(self):
        """ Testing R1-8:
        Billing Address is empty at time of registration.
        """
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        User.register("u01", "test7@test.com", "Onetwo!")
        user = database.User.query.get(1)
        assert user is not None
        assert user.billing_address == ""

    def test_r1_9_user_register(self):
        """ Testing R1-9:
        Postal Code is empty at time of registration.
        """
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        User.register("u09", "test9@test.com", "Onetwo!")
        user = database.User.query.get(1)
        assert user is not None
        assert user.postal_code == ""

    def test_r1_10_user_register(self):
        """ Testing R1-10:
        Balance should be initialized as 100 at time of registration.
        """
        db.session.rollback()
        with app.app_context():
            db.drop_all()
            db.create_all()

        User.register("u10", "test10@test.com", "Onetwo!")
        user = database.User.query.get(1)
        assert user is not None
        assert user.balance == 100

    def test_r2_1_login(self):
        """Test if user can log in using her/his email address and the 
        password.

        Note:
        User.login will return reference to user if login success
        User.login will return 1 if login failure due to invalid username 
                                                                or password
        User.login will return 2 if login failure due to incorrect 
                                                    username or password
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        bob = User()
        bob.email = "bob@gmail.com"
        bob.password = "Password123!"
        bob.add_to_database()

        fred = User()
        fred.email = "fred@gmail.com"
        fred.password = "Password321!"
        fred.add_to_database()

        # assert valid logins don't return None
        assert User.login("bob@gmail.com", "Password123!")
        assert User.login("fred@gmail.com", "Password321!")

        with self.assertRaisesRegex(ValueError,
                                    "Incorrect email or password"):
            User.login("bob@gmail.com", "IncorrectPassword123!")
            User.login("fred@gmail.com", "Password123!")

    def test_r2_2_login(self):
        """Test that the login function should check if the supplied 
        inputs meet the same email/password requirements as above, before 
        checking the database.

        Note:
        User.login will return 0 if login success
        User.login will return 1 if login failure due to invalid username 
                                                                or password
        User.login will return 2 if login failure due to incorrect 
                                                    username or password
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        bob = User()
        bob.email = "bob@gmail.com"
        bob.password = "Password123!"
        bob.add_to_database()

        # assert valid login is not None
        assert User.login("bob@gmail.com", "Password123!")

        with self.assertRaisesRegex(ValueError,
                                    "Invalid email or password"):
            User.login("b.o.b.@gmail..com", "Password123!")
            User.login("bob@gmail.com", "psw")
            User.login("b.o.b.@gmail..com", "psw")

    def test_r3_1_update_user(self):
        """ Testing R3-1:
        A user is only able to update his/her user name, user email,
        billing address, and postal code.
        """
        with database.app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()

        # Update username
        user.update_username("updatedUsername")
        assert user.database_obj.username == "updatedUsername"

        # Update user email
        user.update_email("updated@email.com")
        assert user.database_obj.email == "updated@email.com"

        # Update address
        user.update_billing_address("123 Update")
        assert user.database_obj.billing_address == "123 Update"

        # Update postal code
        user.update_postal_code("A1A1A1")
        assert user.database_obj.postal_code == "A1A1A1"

    def test_r3_2_update_user_profile(self):
        """Testing R3-2: 
        postal code should be non-empty, alphanumeric-only,
        and no special characters such as !.
        """
        with database.app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()

        valid_postal_codes = ["A1A1A1",
                              "N1P0A0", "N1T9Z9", "V0C0A0", "V0C9Z9"]
        for i in valid_postal_codes:
            user.update_postal_code(i)
            assert user.database_obj.postal_code == i

        invalid_postal_codes = ["", "!C1Ajd", "a!a1a1",
                                "AAAAAA", "123904", "ASD2U1",
                                "1A2C3D"]
        for i in invalid_postal_codes:
            with self.assertRaises(ValueError):
                user.update_postal_code(i)

    def test_r3_3_update_user_profile(self):
        """Testing R3-3: 
        Postal code has to be a valid Canadian postal code.
        """
        with database.app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()

        valid_postal_codes = ["A1A1A1", "N1P0A0", "N1T9Z9"]
        for i in valid_postal_codes:
            user.update_postal_code(i)
            assert user.database_obj.postal_code == i

        invalid_postal_codes = ["D1C9E7", "F1A1A1", "I1A1A1", "O1A1A1",
                                "Q1A1A1", "U1A1A1"]
        for i in invalid_postal_codes:
            with self.assertRaises(ValueError):
                user.update_postal_code(i)

    def test_r3_4_update_username(self):
        """Testing R3-4: 
        User name follows the requirements above.
        """
        with database.app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()

        valid_usernames = ["asdhjk", "userName",
                           "USERNAME", "user name", "123 1112 4902"]
        for i in valid_usernames:
            user.update_username(i)
            assert user.database_obj.username == i

        invalid_usernames = ["", " ASD", "! ASD",
                             "as", "1246789012317823678123678678904"]
        for i in invalid_usernames:
            with self.assertRaises(ValueError):
                user.update_username(i)

    def test_r4_1_create_listing(self):
        """Testing R4-1:
        The title of the product has to be alphanumeric-only, 
        and space allowed only if it is not as prefix and suffix.
        """
        with app.app_context():
            db.drop_all()
            db.create_all()

        t1 = "4 bed 2 bath"
        t2 = " 4 bed 2 bath"
        t3 = "4 bed 2 bath "
        t4 = "4 bed 2 bath?"
        assert (Listing.valid_title(t1)) is True
        assert (Listing.valid_title(t2)) is False
        assert (Listing.valid_title(t3)) is False
        assert (Listing.valid_title(t4)) is False

    def test_r4_2_create_listing(self):
        """Testing R4-2:
        The title of the product is no longer than 80
        characters.
        """
        t1 = "a" * 80
        t2 = t1 + "a"
        assert (Listing.valid_title(t1)) is True
        assert (Listing.valid_title(t2)) is False

    def test_r4_3_create_listing(self):
        """Testing R4-3:
        The description of the product can be arbitrary 
        characters, with a minimum length of 20 characters and a 
        maximum of 2000 characters.
        """
        t0 = "qwertyuiopqwertyui"
        des1 = "a" * 2000
        des2 = "qwertyuiopqwertyuiop"
        des3 = "qwertyuiopqwertyu"
        des4 = des1 + "a"
        assert (Listing.valid_description(des1, t0)) is True
        assert (Listing.valid_description(des2, t0)) is True
        assert (Listing.valid_description(des3, t0)) is False
        assert (Listing.valid_description(des4, t0)) is False

    def test_r4_4_create_listing(self):
        """Testing R4-4:
        Description has to be longer than the product's title.
        """
        t0 = "qwertyuiopqwertyuiywqewwqtwqwqe"
        des1 = "a" * 35
        des2 = "a" * 30
        assert (Listing.valid_description(des1, t0)) is True
        assert (Listing.valid_description(des2, t0)) is False

    def test_r4_5_create_listing(self):
        """Testing R4-5: Price has to be of range [10, 10000]."""
        l1 = Listing()
        p1 = 10
        p2 = 10000
        p3 = 9.999999
        p4 = 10000.001
        assert (l1.valid_price(p1)) is True
        assert (l1.valid_price(p2)) is True
        assert (l1.valid_price(p3)) is False
        assert (l1.valid_price(p4)) is False

    def test_r4_6_create_listing(self):
        """Testing R4-6:
        last_modified_date must be after 
        2021-01-02 and before 2025-01-02.
        """
        l1 = Listing()
        d1 = datetime(2021, 1, 2)
        d2 = datetime(2021, 1, 3)
        d3 = datetime(2025, 1, 1)
        d4 = datetime(2025, 1, 2)
        assert (l1.valid_date(d1)) is False
        assert (l1.valid_date(d2)) is True
        assert (l1.valid_date(d3)) is True
        assert (l1.valid_date(d4)) is False

    def test_r4_7_create_listing(self):
        """Testing R4-7:
        owner_email cannot be empty. The owner of the 
        corresponding product must exist in the database.
        """
        u1 = User("bob", "bob69@gmail.com", "pizza")
        u1.add_to_database()
        u2 = User("Ross", "", "pizza")
        u2.add_to_database()
        u3 = User("Tom", "tom69@gmail.com", "pizza")
        u4 = User("Sam", "", "pizza")
        assert (Listing.valid_seller(u1)) is True
        assert (Listing.valid_seller(u2)) is False
        assert (Listing.valid_seller(u3)) is False
        assert (Listing.valid_seller(u4)) is False

    def test_r4_8_create_listing(self):
        """Testing R4-8:
        A user cannot create products that have the same title
        """
        des1 = "Hello, this lovely home has 0 bathrooms"
        p1 = 100.50
        des2 = "Hey, this place sucks."

        l1 = Listing("4 bed 2 bath", des1, p1)
        l1.add_to_database()
        l2 = Listing("4 bed 2 bath", des2, p1)
        l3 = Listing("4 bed 2 baths", des2, p1)
        assert (Listing.valid_title(l2.title)) is False
        assert (Listing.valid_title(l3.title)) is True

    def test_r5_1_update_listing(self):
        """ Testing R5-1:
        One can update all attributes of the listing, except 
        owner_id and last_modified_date.
        """
        # Initialize Listing
        title = "4 Bed 2 Bath"
        address = "Queen's University"
        price = 8000.57
        description = "Best school to ever exist"
        seller = User()
        obj = Listing(title, description, price, seller, address)

        r1 = Review()
        obj.add_review(r1)

        obj.add_to_database()

        # test if changing the title works
        obj.update_title("different title")
        assert obj.database_obj.title == "different title"

        with self.assertRaises(ValueError):
            obj.update_title(" this won't work")

        # test if changing the address works
        obj.address = "different address"
        assert obj.address == "different address"

        # test if changing the price works
        obj.update_price(8100)
        assert obj.database_obj.price / 100 == 8100

        # test if changing the description works
        obj.update_description("different description 12345678")
        assert obj.database_obj.description == "different description 12345678"

        # test that adding review works
        old_reviews = obj.reviews
        r1 = Review()
        obj.add_review(r1)
        old_reviews.append(r1)
        assert obj.reviews == old_reviews

        # test that changing the seller should not work
        old_seller = obj.seller
        with self.assertRaises(ValueError):
            obj.seller = User()
        assert obj.seller == old_seller

    def test_r5_2_update_listing(self):
        """ Testing R5-2:
        Price can be only increased but cannot be decreased.
        """
        with app.app_context():
            db.drop_all()
            db.create_all()
        # Initialize Listing
        title = "4 Bed 2 Bath"
        address = "Queen's University"
        price = 8000.57
        description = "Shittiest school to ever exist"
        seller = User()
        obj = Listing(title, description, price, seller, address)

        # test that price does not change, as change is invalid
        with self.assertRaises(ValueError):
            obj.update_price(1500)
        assert obj.price == 8000.57

        # test that price does change, as change is valid
        obj.price = 8200
        assert obj.price == 8200

        # test that price does not change, as change is invalid
        with self.assertRaises(ValueError):
            obj.price = 8199.99
        assert obj.price == 8200

        # test that price does not change, as there is no change
        with self.assertRaises(ValueError):
            obj.price = 8200
        assert obj.price == 8200

    def test_r5_3_update_listing(self):
        """ Testing R5-3:
        last_modified_date should be updated when the update operation 
        is successful.
        """
        # Initialize Listing
        title = "4 Bed 2 Bath"
        address = "Queen's University"
        price = 8000.57
        description = "Shittiest school to ever exist"
        seller = User()
        obj = Listing(title, description, price, seller, address)

        # used as a margin of error when testing if 2 times are equal
        margin = timedelta(milliseconds=1)

        # test that initializing the listing creates an accurate
        # last_modified_date (aka creation date)
        lower = (datetime.now() - margin).date().isoformat()
        upper = (datetime.now() + margin).date().isoformat()
        assert lower <= obj.modified_date <= upper

        # test that update_title also updates last_modified_date
        old_last_modified_date = obj.modified_date
        obj.title = "new title"
        # test that updated last_modified_date is later than
        # last_modified_date before title was updated
        assert obj.modified_date >= old_last_modified_date
        # test that new last_modified_date is close enough to the current
        # time (margin accounts for execution time)
        lower = (datetime.now() - margin).date().isoformat()
        upper = (datetime.now() + margin).date().isoformat()
        assert lower <= obj.modified_date <= upper

        # test that update_address also updates last_modified_date
        old_last_modified_date = obj.modified_date
        obj.address = "new address"
        # test that updated last_modified_date is later than
        # last_modified_date before address was updated
        assert obj.modified_date >= old_last_modified_date
        # test that new last_modified_date is close enough to the current
        # time (margin accounts for execution time)
        lower = (datetime.now() - margin).date().isoformat()
        upper = (datetime.now() + margin).date().isoformat()
        assert lower <= obj.modified_date <= upper

        # test that update_price also updates last_modified_date
        old_last_modified_date = obj.modified_date
        obj.price = 8500
        # test that updated last_modified_date is later than
        # last_modified_date before price was updated
        assert obj.modified_date >= old_last_modified_date
        # test that new last_modified_date is close enough to the current
        # time (margin accounts for execution time)
        lower = (datetime.now() - margin).date().isoformat()
        upper = (datetime.now() + margin).date().isoformat()
        assert lower <= obj.modified_date <= upper

        # test that if update_price failes, last_modified_date is not
        # updated
        old_last_modified_date = obj.modified_date
        with self.assertRaises(ValueError):
            obj.price = 8500
        # test that last_modified_date didn't changeW
        assert obj.modified_date == old_last_modified_date

        # test that update_description also updates last_modified_date
        old_last_modified_date = obj.modified_date
        obj.description = "new description 123678121212367812637812"
        # test that updated last_modified_date is later than
        # last_modified_date before description was updated
        assert obj.modified_date >= old_last_modified_date
        # test that new last_modified_date is close enough to the current
        # time (margin accounts for execution time)
        lower = (datetime.now() - margin).date().isoformat()
        upper = (datetime.now() + margin).date().isoformat()
        assert lower <= obj.modified_date <= upper

        # test that add_review also updates last_modified_date
        old_last_modified_date = obj.modified_date
        obj.add_review(Review())
        # test that updated last_modified_date is later than
        # last_modified_date before price was updated
        assert obj.modified_date >= old_last_modified_date
        # test that new last_modified_date is close enough to the current
        # time (margin accounts for execution time)
        lower = (datetime.now() - margin).date().isoformat()
        upper = (datetime.now() + margin).date().isoformat()
        assert lower <= obj.modified_date <= upper

    def test_r5_4_update_listing(self):
        """ Testing R5-4:
        When updating an attribute, one has to make sure that it follows 
        the same requirements as above. Mainly the subsections of R4.
        """
        listing = Listing()
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
        listing.title = t1
        assert (listing.title == t1)

        with self.assertRaises(ValueError):
            listing.title = t2
            listing.title = t3
            listing.title = t4
            listing.title = t5

        # Testing Descriptions
        listing.title = "12345678901234567890"
        des1 = ""
        i = 0
        while (i < 2000):
            des1 = des1 + "a"
            i = i + 1
        des2 = "123456789001234567890"
        des3 = "1234567890012345678901"
        des4 = ""
        i = 0
        while (i < 2001):
            des4 = des4 + "a"
            i = i + 1

        listing.description = des1
        assert (listing.description == des1)

        listing.description = des2
        assert (listing.description == des2)

        with self.assertRaises(ValueError):
            listing.description = des3
            listing.description = des4

        # Testing Prices
        p1 = 9.999999
        p2 = 10
        p3 = 10000
        p4 = 10000.001

        listing.price = p2
        assert (listing.price == p2)

        listing.price = p3
        assert (listing.price == p3)

        with self.assertRaises(ValueError):
            listing.price = p4
            listing.price = p1

        # test new title can't be same as existing listing title in
        # database when updating title
        des1 = "Hello, this lovely home has 0 bathrooms"
        p1 = 100.50
        des2 = "Hey, this place sucks."

        l1 = Listing("4 bed 2 bath", des1, p1)
        l1.add_to_database()

        l2 = Listing("4 bed 2 bath(1)", des2, p1)
        with self.assertRaises(ValueError):
            l2.title = "4 bed 2 bath"
        assert l2.title == "4 bed 2 bath(1)"

        l3 = Listing("4 bed 2 baths(2)", des2, p1)
        l3.title = "4 bed 2 baths"
        assert l3.title == "4 bed 2 baths"

    def test_query_and_update(self):
        with app.app_context():
            db.drop_all()
            db.create_all()

        user = User("testUser", "user@example.ca", "password123")
        user.add_to_database()

        queried_user = User.query_user(1)
        assert queried_user.username == "testUser"
        assert queried_user.email == "user@example.ca"
        assert queried_user.password == "password123"

        queried_user.update_billing_address("updating street")
        assert queried_user.billing_address == "updating street"
        assert queried_user.database_obj.billing_address == "updating street"

        queried_again = User.query_user(1)
        assert queried_again.database_obj.billing_address == "updating street"
        queried_again.update_username("ganya")
        assert queried_again.username == "ganya"
        assert queried_again.database_obj.username == "ganya"

        assert queried_user.database_obj.username == "ganya"


if __name__ == "__main__":
    unittest.main()
