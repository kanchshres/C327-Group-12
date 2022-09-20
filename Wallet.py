from Transaction import Transaction

class Wallet:
    def __init__(self):
        self.id = None
        self.balance = 0
        self.bankingAccount = None
        self.transactions: list[Transaction] = []
    
@property
def bankingAccount(self):
    return self._bankingAccount.id

@property
def transactions(self) -> list[Transaction]:
    return self._transactions

@transactions.setter
def transactions(self, values:list[int]):
    if all(isinstance(i, list[Transaction]) for i in values):
        self._transactions = values
    else:
        raise ValueError("values must be a list of Transaction objects")

def add_transaction(self, transaction:Transaction):
    if not isinstance(transaction, Transaction):
        raise ValueError("transaction must be a Transaction object")
    self._transactions.append(transaction)

@property
def __str__(self):
    return str(self.id, self.balance)