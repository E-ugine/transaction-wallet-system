from pydantic import BaseModel, Field, ConfigDict


class CreateAccount(BaseModel):
    owner: str

class AccountResponse(BaseModel):
    id : int
    owner : str    

    model_config = ConfigDict(from_attributes=True)