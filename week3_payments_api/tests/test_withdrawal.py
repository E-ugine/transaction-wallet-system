from models import Account

def test_withdrawal_populates_balance():
    account = Account(owner="Test User")
    account.deposit(500)
    account.withdraw(350)
    assert account.balance() == 150