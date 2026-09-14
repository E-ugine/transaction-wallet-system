from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from schema import AccountResponse,CreateAccount, DepositRequest, DepositResponse, WithdrawalRequest, WithdrawalResponse, TransferRequest, TransferResponse, TransactionResponse
from models import Account, InvalidAmountError, InsufficientFundsError, IdempotencyKey
from database import get_db
from sqlalchemy import select
import hashlib
import datetime
import json

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

     key_query = select(IdempotencyKey).where(IdempotencyKey.key == amount_in.idempotency_key)
     existing_key = db.execute(key_query).scalar_one_or_none()

     if existing_key is not None:
          if existing_key.request_fingerprint != fingerprint:
               raise HTTPException(status_code=409, detail="There was a problem verifying your transfer details. Please refresh the page and try making your payment again.")
          elapsed = datetime.datetime.now() - existing_key.created_at
          is_expired = elapsed > datetime.timedelta(hours=24)

          if not is_expired:
               return TransferResponse(**json.loads(existing_key.response_data))
               
     from_account_query = select(Account).where(Account.id == from_account_id)
     from_account = db.execute(from_account_query).scalar_one_or_none()  

     if from_account is None:
          raise HTTPException(status_code=404, detail="Sender account not found") 

     to_account_query = select(Account).where(Account.id==amount_in.to_account_id)
     to_account = db.execute(to_account_query).scalar_one_or_none()     

     if to_account is None:
          raise HTTPException(status_code=404, detail="The recipient account does not exist")

     else:
          try:
               from_account.withdraw(amount_in.amount)
               to_account.deposit(amount_in.amount)
          except InvalidAmountError:
                          raise HTTPException(status_code=400, detail="You entered an invalid Amount. Please try again!")
          except InsufficientFundsError:
            raise HTTPException(status_code=400, detail="Insufficient Funds in your account!")
          else: 
               response = TransferResponse(message="Transfer Successful", from_balance=from_account.balance())
               serialized_response= response.model_dump_json()
               transaction_key=IdempotencyKey(key=amount_in.idempotency_key, status="Successful", response_data=serialized_response, request_fingerprint=fingerprint)
               db.add(transaction_key)
               db.commit()
               db.refresh(transaction_key)

               return response


@app.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])          
def list_transactions(account_id: int,transaction_type: str | None = None, db: Session=Depends(get_db)):
     query = select(Account).where(Account.id == account_id)
     account = db.execute(query).scalar_one_or_none()

     if account is None:
          raise HTTPException(status_code=404, detail="The account doesn't exist. Please create it first.")
     return [t for t in account.transactions if transaction_type is None or t.transaction_type == transaction_type]
     



               
               

          
          
