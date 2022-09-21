#wallet.py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from transaction import Transaction

class Wallet:
    """Object representation of a digital wallet.
    
    params:
    - id: An UID of the wallet
    - balance: the current account balance
    - bankingAccount: The associated banking account with the wallet
    - transactions: A list of transactions associated with the wallet
    """
    def __init__(self):
        self._id = None
        self._balance: int = 0
        self._bankingAccount: 'BankingAccount' = None
        self._transactions: 'list[Transaction]' = []

    @property
    def __str__(self):
        return str(self._id, self._balance)

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
            raise ValueError("Transfered amount cannot be negative")

        try: 
            self._balance += self.bankingAccount.transfer_balance(amount)
        except ValueError:
            print("")


class BankingAccount:
    """Object representation of a Banking Account

    params:
    id: the account number
    account_holer_name: the name of the account holder
    balance (int): The balance of the Banking Account
    currency: the currency of the balance

    """
    def __init__(self):
        self._id = 0
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
    
    """Subtract balance from current account balance to a transaction

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
        elif amount > self._balance:
            raise ValueError("Unsufficient account balance")
        self._balance -= amount
        return amount

    def add_balance(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("amount must be greater than zero")
        else:
            self._balance += amount
        return amount



def test():
    from user import User
    from wallet import Wallet

    bank_account = BankingAccount()
    user = User()
    user.email = "hello@gbay.com"
    user.username = "hello"
    user.password = "plainstring"
    user.ID = "1234"
    user.wallet = Wallet()
    user.wallet.bankingAccount = bank_account

    bank_account.add_balance(10000)
    assert user.wallet.bankingAccount.balance == 10000

    user._wallet.transfer_balance(5000)
    assert user.wallet.bankingAccount.balance == 5000
    assert user.balance == 5000

test()
