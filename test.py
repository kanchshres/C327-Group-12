from review import Review
from user import User

def test_user():
    test = User()
    print(test.id)
    test.id = 10

    test.email = "shrestha.kanch@gmail.com"
    print(test.email)

    test_rev = Review()
    test_rev._id = 100
    test_rev.date_posted = "2022-09-21"
    test_rev.posting_user = test
    test_rev._listing = None
    test_rev._rating = 5
    test_rev.comment = "Loved this place!"
    test.add_review(test_rev)
    print(test.reviews)
test_user()