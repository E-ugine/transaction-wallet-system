import uuid
import datetime


class InvalidAmountError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class Transaction:
    def __init__(self, amount, transaction_type, ):
        self.id = uuid.uuid4()
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.datetime.now()
        self.status = "Pending"


    def __repr__(self):
        return f"Transaction(id={self.id}, amount={self.amount}, type={self.transaction_type}, status={self.status})"


    def __eq__(self,other):
        if isinstance(other, Transaction):
            return self.id ==other.id
        return False

    def __hash__(self):
        return hash(self.id)

"""t1 = Transaction(20000, "deposit")
t2 = Transaction(20000, "deposit")
print(t1 == t2) """           

class Account:
    def __init__(self, owner):
        self.owner = owner
        self.account_id = uuid.uuid4()
        self.transactions = [] # transactions as a list of objects


    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError(f"You can't deposit zero or a negative amount: {amount}") 
        self.transactions.append(Transaction( amount,"deposit")) 


    def balance(self):
        available_balance = 0
        for transaction in self.transactions:
            if transaction.transaction_type == 'deposit':
                available_balance += transaction.amount
            elif transaction.transaction_type == 'withdraw':
                available_balance -= transaction.amount
        return available_balance


    def withdraw(self, amount):  
        if amount <= 0:
            raise InvalidAmountError("You can't withdraw Ksh 0 or less")
        if (amount > self.balance()):
            raise InsufficientFundsError(f"You have insufficients funds to withdraw: {amount}")
        self.transactions.append(Transaction(amount,"withdraw"))


    def __iter__(self):
        return iter(self.transactions) # iter(self.transactions) is the 'iterator'


"""acc1 = Account("Eugine") 
print(acc1.owner)
acc1.deposit(20000)
acc1.withdraw(999) 
print(acc1.balance())  
for transaction in acc1: print(transaction) """



# Sequencing risk in transfer
# We do withdrawal first before deposit. This ensures we don't have money moving on one side and failing on the other.
# A case is i we do deposit first then withdrawal fails say 'InsufficientError'

class Wallet:

    def __init__(self):
        self.accounts = {}


        
    def register_account(self,account):
        self.accounts[account.account_id] = account


    def transfer(self,from_account, to_account, amount):
        from_account.withdraw(amount)
        to_account.deposit(amount)
        


