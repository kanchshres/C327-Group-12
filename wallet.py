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
    def __str__(self):
        return str(self._id, self._balance)

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

    def transfer_balance(self, amount: int):
        try: 
            self.balance += self.bankingAccount.transfer_balance(amount)
        except ValueError:
            print()


class BankingAccount:
    """
    Object representation of a Banking Account

    params:
    id: the account number
    account_holer_name: the name of the account holder
    balance (int): The balance of the Banking Account
    currency: the currency of the balance

    """
    def __init__(self):
        self.id = 0
        self.account_holer_name = ""
        self.balance: int = 0
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
    
    """
    Subtract balance from current account balance to a transaction

    params:
    amount: the amount to be transfered from the account

    Raises:
        ValueError: When current balance is less than the required balance or if the ammount transfer is less than 0

    Returns:
        amount (int): the transfered amount
    """
    def transfer_balance(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be greater than zero")
        elif amount > self.balance:
            raise ValueError("Unsufficient account balance")
        self.balance -= amount
        return amount

    def add_balance(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be greater than zero")
        else:
            self.balance += amount
        return amount
