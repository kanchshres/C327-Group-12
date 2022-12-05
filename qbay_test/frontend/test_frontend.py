from seleniumbase import BaseCase
from qbay.database import app, db
from qbay.user import User
from qbay_test.conftest import base_url
from unittest.mock import patch
from datetime import datetime

"""
This file defines all Front-end Integration Tests
"""


class FrontEndTests(BaseCase):
    def initialize_database(self):
        # Clear database
        with app.app_context():
            db.drop_all()
            db.create_all()

    def register_helper(self, email, username, password):
        # Register user given email, username, password
        self.open(base_url + '/register')
        self.type("#email", email)
        self.type("#username", username)
        self.type("#password", password)
        self.type("#password2", password)
        self.click('input[type="submit"]')

    def login_helper(self, email, password):
        # Log-in given email, password
        self.open(base_url + '/login')
        self.type("#email", email)
        self.type("#password", password)
        self.click('input[type="submit"]')

    def create_listing_helper(self, title, description, price, address):
        # Create listing given title, description, price
        self.click_link("Create Listing")
        self.type("#title", title)
        self.type("#description", description)
        self.type("#price", price)
        self.type("#address", address)
        self.click('input[type="submit"]')

    def update_listing_helper(self, title, description, price):
        # Update listing given title, description, price
        self.click_link("My Listings")
        self.click_link("Edit")
        self.type("#title", title)
        self.type("#description", description)
        self.type("#price", price)
        self.click('input[type="submit"]')

    def assert_helper(self, element, text, url):
        # Assert given an element, text, and return to desired url
        self.assert_element(element)
        self.assert_text(text, element)
        if (url):
            self.open(url)

    def test_register_input(self, *_):
        # Input coverage testing by input partitioning on username
        # n = length of username
        self.open(base_url + '/register')

        # P1: n < 2
        email, user, password = "test04@test.com", "4", "Onetwo!"
        element, text = "#message", "Registration failed"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)

        # P2: n > 20
        email, user = "test05@test.com", "TestFiveUserNameIsTooLong"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)

        # P3: n = 2
        email, user = "test06@test.com", "u6"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)

        # P4: n = 20
        email, user = "test07@test.com", "Test Seven failure!!"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)

        # P5: 2 < n < 20
        email, user = "test08@test.com", "Test Eight"
        element, text = "#welcome-header", "Login"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)

    def test_register_output(self, *_):
        # Output coverage testing
        self.open(base_url + '/register')

        # Output: Registration fails
        email, user, password = "reg01@test.com", "Test One", "Onetwo!"
        element, text = "#message", "Registration failed"
        self.register_helper(email, "", password)
        self.assert_helper(element, text, None)

        # Output: Registration works
        element, text = "#welcome-header", "Login"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)

    def test_register_functionality(self, *_):
        # Functionality Testing by Requirement Partitioning
        self.open(base_url + '/register')

        # R1: Email and password cannot be empty.
        # R1-T1: Both empty
        user = "Func One Test One"
        element, text = "#message", "Registration failed"
        self.register_helper("", user, "")
        self.assert_helper(element, text, None)
        # R1-T2: Email empty, password not
        user, password = "Func One Test Two", "Onetwo!"
        self.register_helper("", user, password)
        self.assert_helper(element, text, None)
        # R1-T3: Email not empty, password empty
        email, user = "func0103@test.com", "Func One Test Three"
        self.register_helper(email, user, "")
        self.assert_helper(element, text, None)
        # R1-T4: Email not empty, password not empty
        email, user = "func0104@test.com", "Func One Test Four"
        element, text = "#welcome-header", "Login"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, base_url + '/register')

        # R2: Email has to follow addr-spec defined in RFC 5322.
        # R2-T1: Email does not follow
        email, user = "func0201test.com", "Func Two Test One"
        element, text = "#message", "Registration failed"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)
        # R2-T2: Email does follow
        email, user = "func0202@test.com", "Func Two Test Two"
        element, text = "#welcome-header", "Login"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, base_url + '/register')

        # R3: Password meets required complexity.
        # R3-T1: Password does not meet requirements
        email, user = "func0301@test.com", "Func Three Test One"
        element, text = "#message", "Registration failed"
        self.register_helper(email, user, "one2")
        self.assert_helper(element, text, None)
        # R3-T2: Password does meet requirements
        email, user = "func0302@test.com", "Func Three Test Two"
        element, text = "#welcome-header", "Login"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, base_url + '/register')

        # R4: Username meets complexity and criteria
        # R4-T1: Username does not meet requirements
        email, user = "func0401@test.com", " This is Func4Test1!!!"
        element, text = "#message", "Registration failed"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)
        # R4-T2: Username does meet requirements
        email, user = "func0402@test.com", "Func Four Test Two"
        element, text = "#welcome-header", "Login"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, base_url + '/register')

        # R5: If email has been used, operation failed.
        # R5-T1: Email used before
        user = "Func Five Test One"
        element, text = "#message", "Registration failed"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)
        # R5-T2: Email not used before
        email, user = "func0502@test.com", "Func Five Test Two"
        element, text = "#welcome-header", "Login"
        self.register_helper(email, user, password)
        self.assert_helper(element, text, None)

    def test_login_input_coverage(self, *_):
        """ Test login page using input coverage (input partitioning) 
        testing method.
        """
        # Initialize & Set up
        self.initialize_database()
        self.open(base_url + '/register')
        email, user, password = "bob@gmail.com", "Bob", "Password123!"
        self.register_helper(email, user, password)

        # Partition 1: Correct input
        element, text = "#welcome-header", "Welcome Bob!"
        self.login_helper(email, password)
        self.assert_helper(element, text, base_url + '/login')

        # Partition 2: Invalid email
        email, password = "", "Password123!"
        element, text = "#message", "Invalid email or password"
        self.login_helper(email, password)
        self.assert_helper(element, text, None)

        # Partition 3: Invalid password
        email, password = "bob@gmail.com", ""
        element, text = "#message", "Invalid email or password"
        self.login_helper(email, password)
        self.assert_helper(element, text, None)

        # Partition 4: Invalid email and password
        email, password = "", ""
        element, text = "#message", "Invalid email or password"
        self.login_helper(email, password)
        self.assert_helper(element, text, None)

    def test_login_output_coverage(self, *_):
        """ Test login page using output coverage (exhaustive) testing 
        method.
        """
        # Initialize & Set up
        self.initialize_database()
        self.open(base_url + '/register')
        email, username, password = "bob@gmail.com", "Bob", "Password123!"
        self.register_helper(email, username, password)

        # Output: User successfullly logs in in with correct login info
        element, text = "#welcome-header", "Welcome Bob!",
        self.login_helper(email, password)
        self.assert_helper(element, text, base_url + '/login')

        # Output: User inputs invalid email or password such that they
        # do not meet the requirements of a valid email and/or a valid
        # password (Won't even check database).
        email, password = "b.o.b.@gmail..com", "Password123!"
        element, text = "#message", "Incorrect email or password"
        self.login_helper(email, password)
        self.assert_helper(element, text, None)

        # Output: Email and/or password is incorrect, that is, the
        # email and password do not match any entry in the database.
        email, password = "notindatabase@gmail.com", "Password123!"
        self.login_helper(email, password)
        self.assert_helper(element, text, None)

    def test_login_req_coverage(self, *_):
        """Test login page using the requirement partitioning testing 
        method
        """
        # Initialize & Set up
        self.open(base_url + '/register')
        self.initialize_database()
        email, username, password = "bob@gmail.com", "Bob", "Password123!"
        self.register_helper(email, username, password)

        # R2-1: A user can log in using her/his email address and the
        # password.
        element, text = "#welcome-header", "Welcome Bob!"
        self.login_helper(email, password)
        self.assert_helper(element, text, base_url + '/login')

        # R2-2: Shouldn't even check database if email or password is
        # not valid.
        email, password = "b.o.b.@gmail.com", "psw"
        element, text = "#message", "Invalid email or password"
        self.login_helper(email, password)
        self.assert_helper(element, text, None)

    def test_create_listing_input(self, *_):
        """ Input Partitioning """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "createlisting02@test.com", "Create Listing 02"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        a = "101 Palace Place, Suite 330, Boston, MA"
        # Title: Valid   | Description: Valid   | Price: Valid
        t, d, p = "1 Bed 4 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 02!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

        # Title: Valid   | Description: Valid   | Price: Invalid
        t, d, p = "1 Bed 4 Baths", "This is a lovely place", 1
        element, text = "#message", "Invalid Price: 1.0"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Title: Valid   | Description: Invalid | Price: Valid
        t, d, p = "1 Bed 4 Baths", "lol", 100
        element, text = "#message", "Invalid Description: lol"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Title: Invalid | Description: Valid   | Price: Valid
        t, d, p = "1 Bed 4 Bath!", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Title: Valid   | Description: Invalid | Price: Invalid
        t, d, p = "1 Bed 4 Baths", "lol", 1
        element, text = "#message", "Invalid Price: 1.0"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Title: Invalid   | Description: Invalid | Price: Valid
        t, d, p = "1 Bed 4 Bath!", "lol", 100
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Title: Invalid | Description: Valid   | Price: Invalid
        t, d, p = "1 Bed 4 Bath!", "This is a lovely place", 1
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Title: Invalid | Description: Invalid | Price: Invalid
        t, d, p = "1 Bed 4 Bath!", "lol", 1
        element, text = "#message", "Invalid Title: 1 Bed 4 Bath!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

    def test_create_listing_output(self, *_):
        """ Output Coverage """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, password = "createlisting03@test.com", "Onetwo!"
        username = "Create Listing 03"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        a = "101 Palace Place, Suite 330, Boston, MA"
        # Successful Creation
        t, d, p = "5 Bed 3 Bath", "This is a lovely place", 100
        self.create_listing_helper(t, d, p, a)
        element, text = "#welcome-header", "Welcome Create Listing 03!"
        self.assert_helper(element, text, None)

        # Invalid Title
        t, d, p = "5 Bed 3 Bath!", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 5 Bed 3 Bath!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Invalid Description
        t, d, p = "5 Bed 3 Baths", "lol", 100
        element, text = "#message", "Invalid Description: lol"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # Invalid Price
        t, d, p = "5 Bed 3 Baths", "This is a lovely place", 1
        element, text = "#message", "Invalid Price: 1.0"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

    def test_create_listing_requirement(self, *_):
        """ Requirement Partitioning """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "createlisting01@test.com", "Create Listing 01"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        a = "101 Palace Place, Suite 330, Boston, MA"
        # R4-1 : The title of the product has to be alphanumeric-only, and
        #        space allowed only if it is not as prefix and suffix
        # R4-1P: 1 Bed 1 Bath
        t, d, p = "1 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

        # R4-1N: 1 Bath 1 Bath!
        t, d, p = "1 Bed 1 Bath!", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 1 Bed 1 Bath!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # R4-2 : The title of the product is no longer than 80 characters
        # R4-2P: len(title) <= 80
        t, d, p = "2 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

        # R4-2N: 80 < len(title)
        t, d, p = "a" * 81, "This is a lovely place", 100
        element, text = "#message", "Invalid Title: " + t
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # R4-3 : The description of the product can be arbitrary characters,
        #        with a minimum character length of 20 and a maximum of 2000
        # R4-3P: 20 <= len(description) <= 2000
        t, d, p = "3 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

        # R4-3N: len(description) < 20 < 2000
        t, d, p = "3 Bed 1 Baths", "lol", "100"
        element, text = "#message", "Invalid Description: lol"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # R4-4 : Description has to be longer than product's title
        # R4-4P: len(title) < len(description)
        t, d, p = "4 Bed 1 Baths", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

        # R4-4N: len(description) < len(title)
        t, d, p = "This is the listing A", "This is a lovely see", 100
        self.create_listing_helper(t, d, p, a)
        element, text = "#message", "Invalid Description: " + d
        self.assert_helper(element, text, base_url)

        # R4-5 : Price has to be of range [10, 10000]
        # R4-5P: 10 <= price <= 10000
        t, d, p = "5 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

        # R4-5N: 10 < 10000 < price
        t, d, p = "5 Bed 1 Baths", "This is a lovely place", 69420
        element, text = "#message", "Invalid Price: 69420.0"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, base_url)

        # R4-8 : A user cannot create products that have the same title
        # R4-8P: title1 != title2
        t, d, p = "6 Bed 1 Bath", "This is a lovely place", 100
        self.create_listing_helper(t, d, p, a)
        element, text = "#welcome-header", "Welcome Create Listing 01!"
        self.assert_helper(element, text, None)

        # R4-8N: title1 == title2
        t, d, p = "1 Bed 1 Bath", "This is a lovely place", 100
        element, text = "#message", "Invalid Title: 1 Bed 1 Bath"
        self.create_listing_helper(t, d, p, a)
        self.assert_helper(element, text, None)

    def test_listing_update_input(self, *_):
        """ Input Partitioning """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "updatelisting02@test.com", "Listing Update 02"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        # Create Listing
        t, d, p = "4 bed 2 bath", "This is a lovely place", 100
        a = "101 Palace Place, Suite 330, Boston, MA"
        self.create_listing_helper(t, d, p, a)

        # Price decreased.
        t, d, p = t, d, 49.99
        element, text = "#messages", "Invalid Price: 49.99"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Price increased
        t, d, p = t, d, 149.99
        element, text = "#messages", "Price updated successfully: 149.99"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

    def test_listing_update_output(self, *_):
        """ Output Coverage"""
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "updatelisting03@test.com", "Listing Update 03"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        a = "101 Palace Place, Suite 330, Boston, MA"
        # Create Listing
        t, d, p = "5 bed 3 bath", "This is a lovely place", 499.99
        self.create_listing_helper(t, d, p, a)
        # Outputs newly updated listing
        # Sucessful Update
        t, d, p = t, "This is a very lovely place", p
        element = "#messages"
        text = "Description updated successfully: This is a very lovely place"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Failure due to invalid title
        t, d, p = "5 bed 3 bath!", d, p
        element, text = "#messages", "Invalid Title"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Failure due to invalid description
        t, d, p = "5 bed 3 bath", "Good place", p
        element, text = "#messages", "Invalid Description"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # Failure due to invalid price
        t, d, p = t, "This is a very lovely place", 69.99
        element, text = "#messages", "Invalid Price"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

    def test_listing_update_requirement(self, *_):
        """ Requirement Partitioning """
        # Initialize database
        self.initialize_database()

        # Register & Log-in
        email, username = "updatelisting01@test.com", "Update Listing 01"
        password = "Onetwo!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

        a = "101 Palace Place, Suite 330, Boston, MA"
        # Create listing
        t, d, p = "6 Bed 3 Bath", "This is a lovely place", 10
        self.create_listing_helper(t, d, p, a)

        # R5-2 : Price can only be increased but cannot be decreased
        # R5-2P: price1 < price2
        t, d, p = t, d, 11.00
        element, text = "#messages", "Price updated successfully: 11.00"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R5-2N: price2 < price 1
        t, d, p = t, d, 10
        element, text = "#messages", "Invalid Price: 10.0"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R5-3 : last_modified_date should be updated when the update operation
        #        is successful
        self.click_link("My Listings")
        element, text = "#listing", datetime.now().date().isoformat()
        self.assert_helper(element, text, base_url)

        # R5-4 : When updating an attribute, it must follow the same
        #        requirements as when it were created
        # R5-4P: 20 <= price1 < price2 <= 10000
        t, d, p = t, d, 12.00
        element, text = "#messages", "Price updated successfully: 12.00"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, base_url)

        # R5-4N: 20 <= price1 <= 10000 < price2
        t, d, p = t, d, 69420
        element, text = "#messages", "Invalid Price: 69420.0"
        self.update_listing_helper(t, d, p)
        self.assert_helper(element, text, None)

    def initialize(self):
        # clear database
        self.initialize_database()

        # Register & Login with Bob
        self.open(base_url + '/register')
        email, username, password = "bob@gmail.com", "Bob", "Password123!"
        self.register_helper(email, username, password)
        self.login_helper(email, password)

    def test_update_username(self, *_):
        """
        R1-5: Username has to be non-empty, alphanumeric-only,
        and space allowed only if it is not as the prefix or suffix.
        R1-6: Username has to be longer than 2 characters
        and less than 20 characters.
        """
        self.initialize()

        def change_name(name):
            self.type("#username", name)
            self.click('input[type="submit"]')

        self.open(base_url + '/user_update')

        change_name("")
        self.is_text_visible("Please fill out this field.")

        # Input partitioning + shotgun: bad cases
        bad_usernames = [" asdasd",  # Leading white space
                         "asdasd ",  # Trailing white space
                         "aa",  # Boundary: length 2
                         "12345678901234567890",  # Boundary: length 20
                         "!aa",  # Special characters
                         "#$!&*123"]  # Special characters
        for name in bad_usernames:
            change_name(name)
            self.assert_text(name, "#username")

        # Input partitioning + shotgun: good cases
        good_usernames = ["ASD",  # Doundary: Length 3
                          "123 ASD",  # Space
                          "AaDF1231231",  # Mixed
                          "1234567890123456789",  # Boundary: length 19
                          "aa AA  123"]  # Multiple Spaces
        for name in good_usernames:
            change_name(name)
            self.assert_text(name, "#username")

    def test_update_email(self, *_):
        """
        R3-1: The email has to follow addr-spec defined in RFC 5322
        """
        self.initialize()

        def change_email(email):
            self.type("#email", email)
            self.click('input[type="submit"]')

        self.open(base_url + '/user_update')

        change_email("")
        self.is_text_visible("Please fill out this field.")

        # Input partitioning + shotgun: bad cases
        bad_emails = ["Abc.example.com",            # No @
                      "A@b@c@example.com",          # > 1 @
                      'a"b(c)d,e:f;g<h>'            # No special characters
                      'i[j\k]l@example.com',
                      'just"not"right@example.com',  # No qouted strings
                      'this is"not\allowed@example.com',  # No escape sequences
                      'i_like_underscore@but_its'  # No underscore domain
                      '_not_allowed_in_this_part.example.com',
                      'QA[icon]CHOCOLATE[icon]@test.com']       # No icon

        for email in bad_emails:
            change_email(email)
            self.assert_text(email, "#email")

        # Input partitioning + shotgun: good cases
        good_emails = ["simple@example.com",
                       "very.common@example.com",
                       "disposable.style.email.with+symbol@example.com",
                       "disposable_style_email_with_underscores@example.com",
                       "other.email-with-hyphen@example.com",
                       "fully-qualified-domain@example.com",
                       "user.name+tag+sorting@example.com",
                       "x@example.com",
                       "example-indeed@strange-example.com", ]

        for email in good_emails:
            change_email(email)
            self.assert_text(email, "#email")

    def test_update_address(self, *_):
        """
        No requirements...
        """
        print("Yay!", end="")

    def test_update_postal_code(self, *_):
        """
        R3-2: postal code should be non-empty, alphanumeric-only,
        and no special characters such as !.
        R3-3: Postal code has to be a valid Canadian postal code.
        """
        self.initialize()

        def change_postal_code(code):
            self.type("#postal_code", code)
            self.click('input[type="submit"]')

        self.open(base_url + '/user_update')

        # Input partitioning + shotgun: bad cases
        invalid_postal_codes = ["",         # Empty
                                "!C1Ajd",   # Special characters
                                "a!a1a1",   # Special characters
                                "a!a1a1",
                                "AAAAAA",   # No number
                                "123904",   # No letter
                                "ASD2U1",   # Wrong format
                                "1A2C3D",   # Wrong format
                                "Z2T1B8",   # Leading Z
                                "H2T1O3",   # Contains O
                                "A1A1A1A1",  # Too long
                                "A1A1"]     # Too short
        for postal_code in invalid_postal_codes:
            change_postal_code(postal_code)
            self.assert_text("", "#postal_code")

        # Input partitioning + shotgun: good cases
        valid_postal_codes = ["A1A1A1",
                              "N1P0A0",
                              "N1T9Z9",
                              "V0C0A0",
                              "V0C9Z9"]
        for postal_code in valid_postal_codes:
            change_postal_code(postal_code)
            self.assert_text(postal_code, "#postal_code")
