from transaction import Transaction

class TransactionQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, tx: Transaction):
        self.queue.append(tx)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def show_all(self):
        for tx in self.queue:
            print(tx)
