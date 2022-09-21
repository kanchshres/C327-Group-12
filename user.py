#user.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wallet import Wallet


class User():

    def __init__(self):
        self._ID = 0  # should be random unique int, change later
        self._username = ""
        self._email = ""   # should also be unique 
        self._password = ""
        self._wallet = None # user should add balance after account creation

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, id):
        self._ID = id
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        self._username = username

    @property
    def email(self):
        return self._mail

    @email.setter
    def email(self, email):
        self._mail = email
        
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def wallet(self):
        return self._wallet

    @wallet.setter
    def wallet(self, wallet):
        from wallet import Wallet

        if isinstance(wallet, Wallet) or wallet is None:
            self._wallet = wallet
        else:
            raise ValueError("wallet must be an object of type Wallet")

    @property
    def balance(self):
        return self.wallet.balance
