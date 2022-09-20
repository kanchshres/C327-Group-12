#wallet.py
from transaction import Transaction

class Wallet:
    """
    Object representation of a digital wallet.
    
    params:
    - id: An UID of the wallet
    - balance: the current account balance
    - bankingAccount: The associated banking account with the wallet
    - transactions: A list of transactions associated with the wallet
    """
    def __init__(self):
        self.id = None
        self.balance = 0
        self.bankingAccount: BankingAccount = None
        self.transactions: list[Transaction] = []

    @property
    def bankingAccount(self):
        return self._bankingAccount.id

    @bankingAccount.setter
    def bankingAccount(self, account):
        self._bankingAccount = account

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
        return str(self._id, self._balance)

    def transfer_balance(self, amount: int):
        try: 
            self.balance += self.bankingAccount.transfer_balance(amount)
        except ValueError:
            print()


class BankingAccount:
    def __init__(self):
        self.id = 0
        self.balance = 0
        self.account_holer_name = ""
        self.currency = ""
    
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self.id = value

    @property
    def balance(self):
        return self._balance
    
    def transfer_balance(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be greater than zero")
        elif amount > self.balance:
            raise ValueError("Unsufficient account balance")
        elif amount >= 0:
            self.balance -= amount
        return amount
    
    def add_balance(self, amount: int):
        if amount < 0:
            raise ValueError("amount must be greater than zero")
        else:
            self.balance += amount
        return amount