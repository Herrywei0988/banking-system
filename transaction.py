class Transaction:
    def __init__(self, tx_type, account_id, amount, target_id=None):
        self.tx_type = tx_type  # 'deposit', 'withdraw', 'transfer'
        self.account_id = account_id
        self.amount = amount
        self.target_id = target_id

    def __repr__(self):
        base = f"{self.tx_type.upper()} | {self.account_id} | ${self.amount}"
        return base + (f" → {self.target_id}" if self.target_id else "")
