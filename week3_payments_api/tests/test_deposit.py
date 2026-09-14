from models import Account


def test_deposit_updates_balance():
    account = Account(owner="Test User")
    account.deposit(500)
    assert account.balance() == 500