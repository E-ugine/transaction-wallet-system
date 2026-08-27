# A Command Line Interface(CLI) that allows deposits, withdrawals, balance checks and transaction filtering by type(deposit/withdrawal)

# The main goal is to build this layer manually without the use of any AI tool. Maybe for consulting but not writing code.

# Transaction fields include: 
     # 1. Transaction ID as INT
     # Amount as DECIMAL
     # Type as String(enum)
     # Date as datetime

Here's the full build sequence for this phase:

# Step 1 
Define the transaction shape (on paper/notes, not code)
Write out exactly what fields a transaction has: transaction ID, account identifier, amount, type (deposit/withdrawal), date. Decide the type of each field (is amount a float or should it be handled more carefully given it's money? is date a string or a datetime object?). This is a decision exercise, not typing.

# Step 2 
Set up the in-memory ledger
Create the empty structure that will hold transactions while the program runs, your list of transaction dicts. No file, no CLI yet. Just the container.

# Step 3
Build add_deposit, no validation yet
Write the function that takes an amount, creates a transaction dict of type "deposit," and appends it to the ledger. Run it manually a few times with plain valid inputs and check the ledger list looks right.

# Step 4 
Build calculate_balance
Write the function that loops through the ledger and computes the net balance, deposits add, withdrawals subtract. Test it against the deposits you added in Step 3 and confirm the number is correct by hand.

# Step 5
Add validation to deposits
Now go back to add_deposit and add the guard: reject amounts below Ksh. 1. Deliberately test it by trying to deposit 0 and a negative number, and confirm it fails the way you intended, this is where your exception handling comes in.

# Step 6
Build add_withdrawal, no validation yet
Same pattern as Step 3, but type "withdrawal." Test manually with valid inputs, confirm calculate_balance correctly reflects the subtraction.

# Step 7
Add validation to withdrawals
Add the guard against withdrawing more than the current balance. Test it by deliberately trying to overdraw and confirming the right exception fires.

# Step 8
Build listing and filtering
Write the function that lists all transactions, then extend it (or add a second function) to filter by type. Test both against the ledger you've built up from Steps 3-7.

# Step 9
Add persistence (save/load to JSON)
Only now, once everything above works purely in memory, add functions to save the ledger to a file and reload it. Test by saving, restarting your program (or clearing the in-memory list), reloading, and confirming the ledger and balance match what they were before.

# Step 10
Build the CLI shell last
Wire up input prompts or a menu that calls the functions you've already proven work. This layer should feel almost mechanical, since all the real logic is already tested.

At each step: write it, run it by hand with a couple of inputs (including a deliberate failure case once validation exists), and don't move to the next step until the current one behaves the way you expect.    