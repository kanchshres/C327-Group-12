#transaction.py
from enum import Enum, unique

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from user import User
    from listing import Listing


@unique
class TransactionStatus(Enum):
    'IN_PROGRESS'
    'DECLINED'
    'CANCELLED'
    'COMPLETED'

class Transaction:
    """
    This is a transaction object that can be used to represent a transaction between two users.
    
    params:
    - **myID**: The transaction id.
    """
    def __init__(self):
        self.id = None
        self.payer: 'User' = None
        self.payee: 'User' = None
        self.amount: 'int' = 0
        self.listing: 'Listing' = None
        self.status: 'TransactionStatus' = None
    
    def __str__(self):
        return str(self._id)
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def payer(self) -> 'User':
        return self._payer
    
    @payer.setter
    def payer(self, value: 'User'):
        self._payer = value
    
    @property
    def payee(self) -> 'User':
        return self._payee
    
    @payee.setter
    def payee(self, value: 'User'):
        self._payee = value

    @property
    def status(self) -> 'TransactionStatus':
        return self._status

    @status.setter
    def status(self, value: 'TransactionStatus'):
        self._status = value
