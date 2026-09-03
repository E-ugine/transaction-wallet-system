from database import SessionLocal
from models import Account
from sqlalchemy import select

with SessionLocal() as session:
    session.add(Account(owner= "Eugine"))
    session.commit()

with SessionLocal() as session:    
    query = select(Account).where(Account.owner == "Eugine")
    result = session.execute(query).scalars().all()

print(result)    