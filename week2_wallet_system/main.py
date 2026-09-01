import uuid
import datetime
import random


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


def retry(func):
    def wrapper(*args, **kwargs):
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == 2:  # Last attempt
                    print(f"[RETRY] {func.__name__} failed permanently")
                    raise e
                print(f"[RETRY] {func.__name__} failed, retrying...")

    return wrapper
    

@retry
def process_payment():
    value = random.random()
    print(f"Generated value: {value:.2f}")
    
    # If statement to simulate a failure condition
    if value < 0.8:
        raise ValueError("Value is too low! Retrying...")
        
    return "Success!"

result = process_payment()
#print(result)
    

class BatchTransaction:
    def __init__(self, account):
        #Stores the account object that this batch will operate on.
        self.account = account
        self.snapshot = None

    def __enter__(self):
        
        #Takes a point-in-time snapshot of the transactions list 
        #and returns the account so it can be used inside the with block.
        self.snapshot = self.account.transactions.copy()
        return self.account

    def __exit__(self, exc_type, exc_val, exc_tb):
        
        #Handles context cleanup. Rolls back changes if an exception occurs
        #and propagates the error by returning False.
       
        if exc_type is not None:
            # An error occurred inside the with block, roll back to the snapshot
            print(f"[BATCH] Error detected ({exc_type.__name__}). Rolling back transactions...")
            self.account.transactions = self.snapshot
        else:
            print("[BATCH] Transaction batch completed successfully.")
            
        # Returning False ensures the exception propagates up to be handled properly
        return False

# Test Example
failure_account = Account("Eugine Failure")
failure_account.deposit(5000)
print(f"Starting Balance: Ksh {failure_account.balance()}")
print(f"Initial Ledger State: {failure_account.transactions}")

# Execute batch with an intentional failure inside a try/except to catch propagation
try:
    with BatchTransaction(failure_account) as acc:
        acc.deposit(20000)
        print(f"Mid-batch Balance (Temporary): Ksh {acc.balance()}")
        
        # Triggering a deliberate error
        acc.withdraw(40000) 
except InsufficientFundsError as e:
    print(f"Caught Propagated Exception: {e}")

#  the ledger  should successfully roll back to its exact pre-batch state
print(f"\nPost-Failure Balance: Ksh {failure_account.balance()}")
print("Post-Failure Ledger State:")
for tx in failure_account:
  print(f" - {tx}")    


 # Test example       
"""pesa = Wallet()     
account1 = Account("Eugine")
account2 = Account("Agolla")   
pesa.register_account(account1)
pesa.register_account(account2)
account1.deposit(18000)
pesa.transfer(account1, account2, 5000)
print(account1.balance())
print(account2.balance())"""


