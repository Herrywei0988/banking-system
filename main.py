import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from transaction import Transaction
from transaction_queue import TransactionQueue

# Create a queue and add three transactions
q = TransactionQueue()
q.enqueue(Transaction("deposit", "A001", 100))
q.enqueue(Transaction("withdraw", "A001", 30))
q.enqueue(Transaction("transfer", "A001", 50, "A002"))

# Display all pending transactions
print(" Pending Transactions:")
q.show_all()

# Processing transactions
print("\n Processing Transactions:")
while not q.is_empty():
    tx = q.dequeue()
    print("Processed:", tx)
