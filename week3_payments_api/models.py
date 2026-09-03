from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DECIMAL, DateTime, ForeignKey

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "accounts"

    id : Mapped[int] = mapped_column(primary_key=True)
    owner : Mapped[str] = mapped_column(String(100))
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account")
    # List tells SQLAlchemy that this is a 1:M relationship. No lists signals M:1/1:1

    def __repr__(self):
        return f"Account(id = { self.id}, owner = {self.owner})"


class Transaction(Base):
    __tablename__ = "transactions"

    id : Mapped[int] = mapped_column(primary_key=True)
    amount : Mapped[DECIMAL] = mapped_column(DECIMAL(10,2))
    transaction_type : Mapped[str] = mapped_column(String(100))
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    status : Mapped[str] = mapped_column(String(100))

    account_id : Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    account: Mapped["Account"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f"Transaction(id = {self.id},amount={self.amount}, transaction_type={self.transaction_type}, timestamp={self.timestamp},status={self.status})"

