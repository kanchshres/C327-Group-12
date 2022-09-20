from enum import Enum, unique
import User

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
        self.payer = None
        self.payee = None
        self.amount = 0
        self.listing = None
        self.status = None
    
    def __str__(self):
        return str(self._id)
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def payer(self):
        return self._payer
    
    @payer.setter
    def payer(self, value):
        if not isinstance(value, User):
            raise ValueError('payer must be a User')
        self._payer = value
    
    @property
    def payee(self):
        return self._payee
    
    @payee.setter
    def payee(self, value):
        if not isinstance(value, User):
            raise ValueError('payee must be a User')
        self._payee = value
        

    @property
    def status(self):
        return self.status.name

    @status.setter
    def status(self, value):
        if value in TransactionStatus:
            self.status = TransactionStatus[value]
        else:
            raise ValueError("Invalid status of TransactionStatus: %s" % value)