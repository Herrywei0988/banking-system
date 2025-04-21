class BankAccount:
    def __init__(self, account_id, name, balance=0):
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f"Deposited ${amount}")
        print(f"[{self.account_id}] Deposit ${amount} | Balance: ${self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"[{self.account_id}] Insufficient funds for withdrawal.")
            return False
        self.balance -= amount
        self.history.append(f"Withdrew ${amount}")
        print(f"[{self.account_id}] Withdraw ${amount} | Balance: ${self.balance}")
        return True

    def transfer(self, target_account, amount):
        if self.withdraw(amount):
            target_account.deposit(amount)
            self.history.append(f"Transferred ${amount} to [{target_account.account_id}]")
            print(f"[{self.account_id}] Transferred ${amount} to [{target_account.account_id}]")
            return True
        return False

    def show_history(self):
        print(f"Transaction history for [{self.account_id} - {self.name}]:")
        for record in self.history:
            print(" -", record)
