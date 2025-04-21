import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction import Transaction
from transaction_queue import TransactionQueue
from account import BankAccount
from faker import Faker
fake = Faker()

# Dictionary to store accounts
accounts = {}

# Transaction queue
q = TransactionQueue()

print(" Welcome to the Bank System!")
print("Available commands: create, deposit, withdraw, transfer, queue, process, show, generate, generate_tx, exit")


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
        print("Transaction added to queue.")

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

    elif command == "generate":
        try:
            count = int(input("How many fake accounts to generate? ").strip())
        except ValueError:
            print("Invalid number.")
            continue

        for i in range(count):
            acc_id = f"A{100 + len(accounts) + i}"
            name = fake.name()
            balance = fake.random_int(min=100, max=1000)
            accounts[acc_id] = BankAccount(acc_id, name, balance)
            print(f"Created [{acc_id}] {name} with balance ${balance}")

    elif command == "generate_tx":
        try:
            num_tx = int(input("How many fake transactions? ").strip())
        except ValueError:
            print("Invalid number.")
            continue

        acc_ids = list(accounts.keys())
        if len(acc_ids) < 2:
            print("Need at least 2 accounts to generate fake transactions.")
            continue

        for _ in range(num_tx):
            tx_type = fake.random_element(elements=("deposit", "withdraw", "transfer"))
            from_acc = fake.random_element(elements=acc_ids)
            amount = fake.random_int(min=10, max=300)

            if tx_type == "transfer":
                to_acc = fake.random_element(elements=[a for a in acc_ids if a != from_acc])
                q.enqueue(Transaction(tx_type, from_acc, amount, to_acc))
            else:
                q.enqueue(Transaction(tx_type, from_acc, amount))

        print(f"Added {num_tx} fake transactions to the queue.")


    elif command == "exit":
        print("Exiting system. Goodbye!")
        break

    else:
        print("Unknown command. Please try again.")
