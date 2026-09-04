from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from schema import AccountResponse,CreateAccount
from models import Account
from database import get_db

app = FastAPI()

@app.post("/accounts", response_model=AccountResponse)
def create_account(account_in: CreateAccount,  db: Session = Depends(get_db) ):
    new_account = Account(owner=account_in.owner)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account    