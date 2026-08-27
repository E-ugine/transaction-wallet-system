import json

from main import add_deposit, check_balance, add_withdrawal, list_transactions, save_ledger, load_ledger, InvalidAmountError, InsufficientFundsError

load_ledger()

while True:
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check Account Balance")
    print("4. View Your Transactions")
    print("5. Exit")
    choice = int(input("Select Option To Proceed:"))

    if choice == 1:
        amount = int(input("Enter Amount:"))
        try:
            add_deposit(amount)
        except InvalidAmountError:
            print(f"You can't deposit zero or a negative amount: {amount}")
        else:
            print("Deposit Successful.")    
            save_ledger()

    elif choice == 2:
        amount = int(input("Enter Amount:"))
        try:
             add_withdrawal(amount)
        except InvalidAmountError:
            print(f"You can't withdraw Ksh 0 or less: {amount}")
        except InsufficientFundsError:
            print(f"You have insufficients funds to withdraw {amount}" )   
        else:
            print("Withdrawal Successful.")    
            save_ledger()


    elif choice == 3:
        print("Your account balance is", check_balance())

    elif choice == 4:
        print("1: View all Transactions")
        print("2: View Deposits")
        print("3: View Withdrawals")
        sub_choice = int(input("Select Option To View:"))

        if sub_choice == 1:
            list_transactions()
        elif sub_choice ==2:
            list_transactions(action="deposit")
        elif sub_choice == 3: 
            list_transactions(action="withdrawal")    
        else:
            print("Invalid Choice! Try Again")

    elif choice == 5:
        break




