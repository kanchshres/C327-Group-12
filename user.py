#user.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wallet import Wallet


class User():

    def __init__(self, id = 0, username: str = "", email: str = "", password: str = ""):
        self._ID = id  # should be random unique int, change later
        self._username: str = username
        self._email: str = email   # should also be unique 
        self._password = password
        self._wallet: Wallet = None # user should add wallet after account creation

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, id):
        self._ID = id
    
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def email(self) -> str:
        return self._mail

    @email.setter
    def email(self, email: str):
        self._mail = email
        
    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = password

    @property
    def wallet(self) -> 'Wallet':
        return self._wallet

    @wallet.setter
    def wallet(self, wallet: 'Wallet'):
        self._wallet = wallet

    @property
    def balance(self):
        return self.wallet.balance
