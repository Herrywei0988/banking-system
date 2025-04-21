import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction import Transaction
from transaction_queue import TransactionQueue
from account import BankAccount

# Dictionary to store accounts
accounts = {}

# Transaction queue
q = TransactionQueue()

print(" Welcome to the Bank System!")
print("Available commands: create, deposit, withdraw, transfer, queue, process, show, exit")

while True:
    command = input("\n>> ").strip().lower()

    if command == "create":
        acc_id = input("Account ID: ").strip()
        name = input("Name: ").strip()
        try:
            balance = float(input("Initial balance: ").strip())
        except ValueError:
            print("Invalid balance.")
            continue
        accounts[acc_id] = BankAccount(acc_id, name, balance)
        print(f"Created account [{acc_id}] for {name} with balance ${balance}")

    elif command == "deposit":
        acc_id = input("Account ID: ").strip()
        if acc_id not in accounts:
            print("Account not found.")
            continue
        amount = float(input("Amount: ").strip())
        accounts[acc_id].deposit(amount)

    elif command == "withdraw":
        acc_id = input("Account ID: ").strip()
        if acc_id not in accounts:
            print("Account not found.")
            continue
        amount = float(input("Amount: ").strip())
        accounts[acc_id].withdraw(amount)

    elif command == "transfer":
        from_id = input("From Account ID: ").strip()
        to_id = input("To Account ID: ").strip()
        if from_id not in accounts or to_id not in accounts:
            print("One or both accounts not found.")
            continue
        amount = float(input("Amount: ").strip())
        accounts[from_id].transfer(accounts[to_id], amount)

    elif command == "queue":
        tx_type = input("Type (deposit/withdraw/transfer): ").strip().lower()
        acc_id = input("Account ID: ").strip()
        amount = float(input("Amount: ").strip())
        target_id = None
        if tx_type == "transfer":
            target_id = input("Target Account ID: ").strip()
        q.enqueue(Transaction(tx_type, acc_id, amount, target_id))
        print("✅ Transaction added to queue.")

    elif command == "process":
        print("\nProcessing Transactions:")
        while not q.is_empty():
            tx = q.dequeue()
            print("Processing:", tx)

            if tx.account_id not in accounts:
                print(f"Account {tx.account_id} not found.")
                continue

            account = accounts[tx.account_id]

            if tx.tx_type == "deposit":
                account.deposit(tx.amount)

            elif tx.tx_type == "withdraw":
                account.withdraw(tx.amount)

            elif tx.tx_type == "transfer":
                if tx.target_id not in accounts:
                    print(f"Target account {tx.target_id} not found.")
                    continue
                target = accounts[tx.target_id]
                account.transfer(target, tx.amount)

    elif command == "show":
        for acc in accounts.values():
            acc.show_history()

    elif command == "exit":
        print("Exiting system. Goodbye!")
        break

    else:
        print("Unknown command. Please try again.")
