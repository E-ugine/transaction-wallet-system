from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import AccountResponse,CreateAccount, DepositRequest, DepositResponse, WithdrawalRequest, WithdrawalResponse, TransferRequest, TransferResponse
from models import Account, InvalidAmountError, InsufficientFundsError
from database import get_db
from sqlalchemy import select
import hashlib

app = FastAPI()


@app.post("/accounts", response_model=AccountResponse)
def create_account(account_in: CreateAccount,  db: Session = Depends(get_db) ):
    new_account = Account(owner=account_in.owner)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account    


@app.post("/accounts/{account_id}/deposit", response_model=DepositResponse)
def make_deposit(account_id: int, amount_in : DepositRequest, db: Session = Depends(get_db)):
    query = select(Account).where(Account.id == account_id)
    result = db.execute(query).scalar_one_or_none()

    if result is None:
        raise HTTPException(status_code=404, detail="Account Not Found!")
    else: 
        try:
            result.deposit(amount_in.amount)
        except InvalidAmountError:
            raise HTTPException(status_code=400, detail="Bad Request")
        else:
            db.commit()  
            return DepositResponse(message="Deposit Successful", balance=result.balance())   


@app.post("/accounts/{account_id}/withdraw", response_model=WithdrawalResponse)
def make_withdrawal(account_id: int, amount_in : WithdrawalRequest, db: Session=Depends(get_db)):  
    query = select(Account).where(Account.id == account_id)
    result = db.execute(query).scalar_one_or_none() 

    if result is None:
            raise HTTPException(status_code=404, detail="Account Not Found!")
    else: 
        try:
            result.withdraw(amount_in.amount)
        except InvalidAmountError:
                raise HTTPException(status_code=400, detail="You entered an invalid Amount. Please try again!")
        except InsufficientFundsError:
                raise HTTPException(status_code=400, detail="Insufficient Funds in your account!")
        else:
            db.commit()  
            return WithdrawalResponse(message="Withdrawal Successful", balance=result.balance()) 



@app.post("/accounts/{from_account_id}/transfer", response_model=TransferResponse)
def wire_transfer(from_account_id: int, amount_in: TransferRequest, db: Session=Depends(get_db)):

     data = f"{from_account_id}-{amount_in.to_account_id}-{amount_in.amount}"
     fingerprint = hashlib.sha256(data.encode()).hexdigest()
