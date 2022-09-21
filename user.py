#user.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wallet import Wallet


class User():

    def __init__(self):
        self.ID = 0  # should be random unique int, change later
        self.username = ""
        self.email = ""   # should also be unique 
        self.password = ""
        self.wallet = None # user should add balance after account creation

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

        if isinstance(wallet, Wallet):
            self._wallet = wallet
        elif wallet is None:
            self._wallet = None
        else:
            raise ValueError("wallet must be an object of type Wallet")

    @property
    def balance(self):
        return self.wallet.balance
