class Account:
    def __init__(self, user_id, balance):
        self.user_id = user_id
        self.balance = balance

def transfer(accountA, accountB, amount):
    if amount <= 0:
        raise ValueError("Amount must be positive")
    if accountA.balance < amount:
        raise ValueError("Insufficient balance")
    accountA.balance -= amount
    accountB.balance += amount