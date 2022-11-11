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
            # If new name is invalid then it remains unchanged
            self.assert_text("Bob", "#username")

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
        R1-3: The email has to follow addr-spec defined in RFC 5322
        """
        self.initialize()

        def change_email(email):
            self.type("#email", email)
            self.click('input[type="submit"]')

        self.open(base_url + '/user_update')

        change_email("")
        self.is_text_visible("Please fill out this field.")

        # Input partitioning + shotgun: bad cases
        bad_emails = ["Abc.example.com",                        # No @
                      "A@b@c@example.com",                      # > 1 @
                      # No special characters
                      'a"b(c)d,e:f;g<h>i[j\k]l@example.com',
                      'just"not"right@example.com',  # No qouted strings
                      'this is"not\allowed@example.com',  # No escape sequences
                      'i_like_underscore@but_its'  # No underscore domain
                      '_not_allowed_in_this_part.example.com',
                      'QA[icon]CHOCOLATE[icon]@test.com']       # No icon

        for email in bad_emails:
            change_email(email)
            self.assert_text("bob@gmail.com", "#email")

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
        print("Yay!")

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
                              "A1A 1A1",
                              "N1P0A0",
                              "N1T9Z9",
                              "V0C0A0",
                              "V0C9Z9"]
        for postal_code in valid_postal_codes:
            change_postal_code(postal_code)
            self.assert_text(postal_code, "#postal_code")
