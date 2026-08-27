import uuid
import datetime


class Transaction:
    def __init__(self, amount, transaction_type, ):
        self.id = uuid.uuid4()
        self.amount = amount
        self.transaction_type = transaction_type
        self.timestamp = datetime.datetime.now()
        self.status = "Pending"


    def __repr__(self):
        return f"{self.amount} {self.transaction_type}"


    def __eq__(self,other):
        if isinstance(other, Transaction):
            return self.id ==other.id
        return False

    def __hash__(self):
        return hash(self.id)

t1 = Transaction(20000, "Deposit")
print(t1)            