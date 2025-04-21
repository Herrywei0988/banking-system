import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction import Transaction
from transaction_queue import TransactionQueue
from account import BankAccount

# Establish an account management system
accounts = {
    "A001": BankAccount("A001", "Alice", 500),
    "A002": BankAccount("A002", "Bob", 300)
}

# Create a transaction queue
q = TransactionQueue()
q.enqueue(Transaction("deposit", "A001", 100))
q.enqueue(Transaction("withdraw", "A001", 200))
q.enqueue(Transaction("transfer", "A001", 150, "A002"))
q.enqueue(Transaction("withdraw", "A002", 500))  # make the balance insufficient

# Display all queued transactions
print(" Pending Transactions:")
q.show_all()

# Execute transaction
print("\n Processing Transactions:")
while not q.is_empty():
    tx = q.dequeue()
    print("Processing:", tx)

    if tx.account_id not in accounts:
        print(f" Account {tx.account_id} not found.")
        continue

    account = accounts[tx.account_id]

    if tx.tx_type == "deposit":
        account.deposit(tx.amount)

    elif tx.tx_type == "withdraw":
        account.withdraw(tx.amount)

    elif tx.tx_type == "transfer":
        if tx.target_id not in accounts:
            print(f" Target account {tx.target_id} not found.")
            continue
        target = accounts[tx.target_id]
        account.transfer(target, tx.amount)

# Display transaction records for each account
print("\n Final Account History:")
for acc in accounts.values():
    acc.show_history()

