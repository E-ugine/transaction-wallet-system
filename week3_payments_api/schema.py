from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class CreateAccount(BaseModel):
    owner: str

class AccountResponse(BaseModel):
    id : int
    owner : str    

    model_config = ConfigDict(from_attributes=True)


class DepositRequest(BaseModel):
    amount : Decimal


class DepositResponse(BaseModel):
    message : str
    balance : Decimal
