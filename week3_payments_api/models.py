from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DECIMAL, DateTime, ForeignKey, Text
import datetime

class Base(DeclarativeBase):
    pass


class InvalidAmountError(Exception):
    pass

class InsufficientFundsError(Exception):
    pass

class Account(Base):
    __tablename__ = "accounts"

    id : Mapped[int] = mapped_column(primary_key=True)
    owner : Mapped[str] = mapped_column(String(100))
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")
    # List tells SQLAlchemy that this is a 1:M relationship. No lists signals M:1/1:1

    def __repr__(self):
        return f"Account(id = { self.id}, owner = {self.owner})"

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError(f"You can't deposit zero or a negative amount: {amount}") 
        self.transactions.append(Transaction( amount=amount,transaction_type="deposit")) 
    
    
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
        self.transactions.append(Transaction(amount=amount,transaction_type="withdraw"))


class Transaction(Base):
    __tablename__ = "transactions"

    id : Mapped[int] = mapped_column(primary_key=True)
    amount : Mapped[DECIMAL] = mapped_column(DECIMAL(10,2))
    transaction_type : Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now)
    status : Mapped[str] = mapped_column(String(100), default="Pending")

    account_id : Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id = {self.id},amount={self.amount}, transaction_type={self.transaction_type}, timestamp={self.timestamp},status={self.status})"


class IdempotencyKey(Base):
    __tablename__ = "idempotencykeys"
    id : Mapped[int] = mapped_column(primary_key=True)
    key : Mapped[str] = mapped_column(String(36), unique=True)
    status : Mapped[str] = mapped_column(String(100), default="Pending")
    response_data : Mapped[str] = mapped_column(Text)
    request_fingerprint : Mapped[str] = mapped_column(String(64))
    created_at : Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now)