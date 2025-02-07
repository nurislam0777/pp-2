class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, money):
        if money > 0:
            self.balance += money
            print(f"+{money} to {self.owner}'s account. Current balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, money):
        if money <= 0:
            print("Withdrawal amount must be positive.")
        elif money > self.balance:
            print(f"Insufficient funds! Current balance: {self.balance}")
        else:
            self.balance -= money
            print(f"-{money} from {self.owner}'s account. Current balance: {self.balance}")

Madiar = Account("Madiar", 5000)

Madiar.deposit(1000)   # Deposit 1000 Balance: 6000
Madiar.withdraw(1500)  # Withdraw 1500 Balance: 4500
Madiar.withdraw(7000)  # Try to withdraw more than the balance Balance: 4500
Madiar.deposit(300)    # Deposit 300 Balance: 4800
Madiar.withdraw(2000)  # Withdraw 2000 Balance: 2800
Madiar.deposit(-100)   # Try to deposit a negative amount Balance: 2800
Madiar.withdraw(-500)  # Try to withdraw a negative amount Balance: 2800



