import selenium
from seleniumbase import BaseCase

from qbay.database import app, db
from qbay.user import User
from qbay_test.conftest import base_url

"""
This file defines all integration tests for the frontend registration page.
"""


class FrontEndTests(BaseCase):

    def initialize(self):
        # clear database
        with app.app_context():
            db.drop_all()
            db.create_all()

        # Output: User successfullly logs in in with correct login info
        self.open(base_url + '/register')
        self.type("#email", "bob@gmail.com")
        self.type("#username", "Bob")
        self.type("#password", "Password123!")
        self.type("#password2", "Password123!")
        self.click('input[type="submit"]')

        self.type("#email", "bob@gmail.com")
        self.type("#password", "Password123!")
        self.click('input[type="submit"]')

    def test_update_username(self, *_):
        """
        R1-5: Username has to be non-empty, alphanumeric-only, and space allowed only if it is not as the prefix or suffix.
        R1-6: Username has to be longer than 2 characters and less than 20 characters.
        """
        self.initialize()

        def change_name(name):
            self.type("#username", name)
            self.click('input[type="submit"]')

        self.open(base_url + '/user_update')

        change_name("")
        self.is_text_visible("Please fill out this field.")

        bad_usernames = [" asdasd", "asdasd ", "a",
                         "1245678901234567890a", "!aa", "#$!&*123"]
        for name in bad_usernames:
            change_name(name)
            # If new name is invalid then it remains unchanged
            self.assert_text("Bob", "#username")

        good_usernames = ["ASD", "123 ASD", "ASD1231231",
                          "1234567890123456789", "aa AA 123"]
        for name in good_usernames:
            change_name(name)
            self.assert_text(name, "#username")

    def test_update_email(self, *_):
        """
        R1-3: The email has to follow addr-spec defined in RFC 5322
        (see https://en.wikipedia.org/wiki/Email_address for a human-friendly explanation).
        You can use external libraries/imports.
        """
        self.initialize()

        def change_email(email):
            self.type("#email", email)
            self.click('input[type="submit"]')

        self.open(base_url + '/user_update')

        change_email("")
        self.is_text_visible("Please fill out this field.")

        bad_emails = ["Abc.example.com", "A@b@c@example.com", 'a"b(c)d,e:f;g<h>i[j\k]l@example.com', 'just"not"right@example.com'
                      'this is"not\allowed@example.com', 'this\ still\"not\\allowed@example.com', '1234567890123456789012345678901234567890123456789012345678901234+x@example.com'
                      'i_like_underscore@but_its_not_allowed_in_this_part.example.com', 'QA[icon]CHOCOLATE[icon]@test.com']

        for email in bad_emails:
            change_email(email)
            self.assert_text("bob@gmail.com", "#email")

        good_emails = ["simple@example.com", "very.common@example.com", "disposable.style.email.with+symbol@example.com", "other.email-with-hyphen@example.com", "fully-qualified-domain@example.com", "user.name+tag+sorting@example.com",
                       "x@example.com", "example-indeed@strange-example.com"]

        for email in good_emails:
            change_email(email)
            self.assert_text(email, "#email")

    def test_update_address(self, *_):
        """
        No requirements...
        """
        print("Yay!")

    def test_update_postal_code(self, *_):
        """
        R3-2: postal code should be non-empty, alphanumeric-only, and no special characters such as !.
        R3-3: Postal code has to be a valid Canadian postal code.
        """
        self.initialize()

        def change_postal_code(code):
            self.type("#postal_code", code)
            self.click('input[type="submit"]')
        
        self.open(base_url + '/user_update')

        invalid_postal_codes = ["", "!C1Ajd", "a!a1a1",
                                "AAAAAA", "123904", "ASD2U1",
                                "1A2C3D"]
        for postal_code in invalid_postal_codes:
            change_postal_code(postal_code)
            self.assert_text("", "#postal_code")
                

        valid_postal_codes = ["A1A1A1",
                              "N1P0A0", "N1T9Z9", "V0C0A0", "V0C9Z9"]
        for postal_code in valid_postal_codes:
            change_postal_code(postal_code)
            self.assert_text(postal_code, "#postal_code")
