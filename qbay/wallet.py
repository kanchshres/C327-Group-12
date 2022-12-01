# wallet.py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from qbay.transaction import Transaction


class Wallet:
    """Object representation of a digital wallet.

    params:
    - id: An UID of the wallet
    - balance: the current account balance
    - bankingAccount: The associated banking account with the wallet
    - transactions: A list of transactions associated with the wallet
    """

    def __init__(self):
        self._id = -1
        self._balance: int = 100
        self._bankingAccount: 'BankingAccount' = None
        self._transactions: 'list[Transaction]' = []

    def __str__(self):
        return '{self.id}, {self.balance}'.format(self=self)

    @property
    def id(self) -> int:
        return self._id

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def bankingAccount(self) -> 'BankingAccount':
        return self._bankingAccount

    @bankingAccount.setter
    def bankingAccount(self, account: 'BankingAccount'):
        self._bankingAccount = account

    @property
    def transactions(self) -> 'list[Transaction]':
        return self._transactions

    @transactions.setter
    def transactions(self, values: 'list[Transaction]'):
        self._transactions = values

    def add_transaction(self, transaction: 'Transaction'):
        self._transactions.append(transaction)

    def transfer_balance(self, amount: int):
        if amount < 0:
            raise ValueError("Transferred amount cannot be negative")

        self._balance += self.bankingAccount.transfer_balance(amount)


class BankingAccount:
    """Object representation of a Banking Account

    params:
    id: the account number
    account_holer_name: the name of the account holder
    balance (int): The balance of the Banking Account
    currency: the currency of the balance

    """

    def __init__(self):
        self._id = -1
        self._account_holer_name = ""
        self._balance: int = 0
        self._currency = ""

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance = value

    """Subtract balance from current account balance to a transaction

    params:
    amount: the amount to be transferred from the account

    Raises:
        ValueError: When current balance is less than the required balance or 
                    if the amount transfer is less than 0

    Returns:
        amount (int): the transferred amount
    """

    def transfer_balance(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be greater than zero")
        elif amount > self._balance:
            raise ValueError("Insufficient account balance")
        self._balance -= amount
        return amount

    def add_balance(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be greater than zero")
        else:
            self._balance += amount
        return amount
