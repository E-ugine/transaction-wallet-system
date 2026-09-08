from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import AccountResponse,CreateAccount, DepositRequest, DepositResponse
from models import Account, InvalidAmountError
from database import get_db
from sqlalchemy import select

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
    

