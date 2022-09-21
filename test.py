from re import T
from review import Review
from user import User
from listing import Listing
from transaction import Transaction
from wallet import Wallet

def test_user():
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

def test_review():
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

def test_transaction():
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

    
    transact.status = "IN_PROGRESS"
    assert transact.status == "IN_PROGRESS"




test_user()
test_review()
test_transaction()