# transaction.py
from enum import Enum, unique

from typing import TYPE_CHECKING, Union
if TYPE_CHECKING:
    from .user import User
    from .listing import Listing


@unique
class TransactionStatus(Enum):
    IN_PROGRESS = 'transactionInProgress'
    DECLINED = 'transactionDeclined'
    CANCELLED = 'transactionCancelled'
    COMPLETED = 'transactionCompleted'
    NEW_TRANSACTION: Literal['TransactionStatus.NEW_TRANSACTION'] = 'transactionNewTransaction'


class Transaction:
    """Object representation of a transaction between two users
    
    params:
    - ID: The transaction id.
    - payer: Type User who is responsible for making the payment
    - payee: Type User who is receiving the payment
    - amount: The amount to be transferred
    - listing: Type Listing as the subject of the transaction
    - status: Type TransactionStatus()
    """
    def __init__(self):
        self._id = None
        self._payer: 'User' = None
        self._payee: 'User' = None
        self._amount: 'float' = 0
        self._listing: 'Listing' = None
        self._status: 'TransactionStatus' = TransactionStatus.NEW_TRANSACTION
    
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
    def status(self, value: 'Union[str, TransactionStatus]'):
        if isinstance(value, str):
            self._status = TransactionStatus(value)
        elif isinstance(value, TransactionStatus):
            self._status = value
        else:
            raise TypeError("value must be member of enum TransactionStatus")
