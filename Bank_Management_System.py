import random
import datetime

class Bank:
    def __init__(self) -> None:
        self.users = {}
        self.loan_feature = True

    def is_bankrupt(self):
        return self.check_total_available_balance() < 0


class User :
    def __init__(self, bank, name, email, address, account_type, balance = 0) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.balance = balance
        self.account_number = self.generate_account_number()
        self.transaction_history = []
        self.loan_count = 0
        self.bank = bank

    def generate_account_number(self):
        account_number = random.randint(1000000, 9999999)
        return account_number
    
    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append({
            "typr": "deposit",
            "amount": amount,
            "timestamp": datetime.datetime.now()
        })

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("withdrawal amount exceeded")
        else:
            self.balance -= amount
            self.transaction_history.append({
                "typr": "withdraw",
                "amount": amount,
                "timestamp": datetime.datetime.now()
            })
        
    def check_balance(self):
        return self.balance
    
    def check_transaction_history(self):
        return self.transaction_history
    
    def take_loan(self, amount):
        if self.loan_count >= 2:
            raise ValueError("You can only take two loan")
        else:
            self.balance += amount
            self.loan_count += 1
            self.transaction_history.append({
                "typr": "loan",
                "amount": amount,
                "timestamp": datetime.datetime.now()
            })
            
    def transfer_amount(self, to_account_number, amount):
        if to_account_number not in self.bank.users:
            raise ValueError("Account does not exist")
        
        if amount > self.balance:
            raise ValueError("Insufficient Balance")
        else:
            self.balance -= amount
            self.bank.users[to_account_number].balance += amount

            self.transaction_history.append({
                "type": "transfer",
                "amount": amount,
                "to_account_number": to_account_number,
                "timestamp": datetime.datetime.now()
            })

            self.bank.users[to_account_number].transaction_history.append({
                "typr": "transfer",
                "amount": amount,
                "from_account_number": self.account_number,
                "timestamp": datetime.datetime.now()
            })


class Admin:
    def __init__(self, bank) -> None:
        self.bank = bank

    def creat_user_account(self, name, email, address, account_type):
        new_user = User(self.bank, name, email, address, account_type)
        print("Your account number is ", new_user.account_number)
        self.bank.users[new_user.account_number] = new_user

    def delete_user_account(self, account_number):
        if account_number in self.bank.users:
            del self.bank.users[account_number]
        else:
            print(f"Account number {account_number} not found.")

    def see_all_user_account(self):
        return self.bank.users
    
    def check_total_available_balance(self):
        total_balance = 0

        for user in self.bank.users.values():
            total_balance += user.balance

        return total_balance
    
    def check_total_loan_amount(self):
        total_loan_amount = 0

        for user in self.bank.users.values():
            total_loan_amount += user.balance - user.deposit

        return total_loan_amount
    
    def on_off_loan_feature(self, state):
        self.bank.loan_feature = state



bank = Bank()
admin = Admin(bank)

while True:
    print("----------WELCOME---------")
    print("1.User")
    print("2.Admin")
    print("3.Exit")

    op = int(input("Enter an option: "))
    print()

    if op == 1:
        
        while True:
            print('Choose an option:')
            print('1. Create an account')
            print('2. Deposit')
            print('3. Withdraw')
            print('4. See Balance')
            print('5. Take Loan')
            print('6. Transfer Money')
            print('7. See Transaction History')
            print('8. Exit')

            choise = int(input("Enter an option: "))
            print()

            if choise == 1:
                name = input("Enetr your name: ")
                email = input("Enter your email: ")
                address = input("Enter your address: ")
                account_type = input("Enter your account type: ")

                admin.creat_user_account(name, email, address, account_type)

            elif choise == 2:
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter the amount to deposit: "))
                user = bank.users.get(account_number)

                if user:
                    user.deposit(amount)
                else:
                    print("Account not found")

            elif choise ==3:
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter the amount to deposit: "))
                user = bank.users.get(account_number)

                if user:
                    try:
                        user.withdraw(amount)
                    except ValueError as e:
                        print(e)

            elif choise == 4:
                account_number = int(input("Enter your account number: "))
                user = bank.users.get(account_number)

                if user:
                    print(f'Your account balance is ${user.check_balance()}')
                else:
                    print("account not found")

            elif choise == 5:
                account_number = int(input("Enter your account number: "))
                amount = int(input("Enter the amount to deposit: "))
                user = bank.users.get(account_number)

                if user:
                    try:
                        user.take_loan(amount)
                    except ValueError as e:
                        print(e)

            elif choise == 6:
                account_number = int(input("Enter your account number: "))
                to_account_number = int(input("Enter to account number: "))
                amount = int(input("Enter the amount to deposit: "))
                user = bank.users.get(account_number)
                to_user = bank.users.get(to_account_number)

                if user and to_user:
                    try:
                        user.transfer_amount(to_account_number, amount)
                    except ValueError as e:
                        print(e)

            elif choise == 7:
                account_number = int(input("Enter your account number: "))
                user = bank.users.get(account_number)

                if user:
                    transactions = user.check_transaction_history()
                    for transaction in transactions:
                        print(f"Type: {transaction['type']} Amount: {transaction['amount']}, Timestamp: {transaction['timestamp']}")
                else:
                    print("Account not found")

            elif choise == 8:
                break

    elif op == 2:
        
        while True:
            print("Choose an option:")
            print('1. Create a user account')
            print('2. See all user accounts')
            print('3. Delete a user account')
            print('4. Check total available balance')
            print('5. Check total loan amount')
            print('6. Loan feature')
            print('7. Exit')

            choise = int(input("Enter an option: "))
            print()

            if choise == 1:
                name = input("Enetr your name: ")
                email = input("Enter your email: ")
                address = input("Enter your address: ")
                account_type = input("Enter your account type: ")

                admin.creat_user_account(name, email, address, account_type)

            elif choise == 2:
                all_users = admin.see_all_user_account()
                for account_number, user in all_users.items():
                    print(f"Account Number: {account_number}, User: {user.name}, Email: {user.email}")

            elif choise ==3:
                account_number = int(input("Enter the account number to delete: "))
                admin.delete_user_account(account_number)

            elif choise == 4:
                total_balance = admin.check_total_available_balance()
                print(f"Total balance of the bank is: ${total_balance}")

            elif choise == 5:
                total_loan_amount = admin.check_total_loan_amount()
                print(f"Total loan in the Bank : ${total_loan_amount}")

            elif choise == 6:
                state = input("Enter 'on' to enable loan feature , 'off' to disable: ")
                if state == 'on':
                    admin.on_off_loan_feature(True)
                elif state == 'off':
                    admin.on_off_loan_feature(False)

            elif choise == 7:
                break

    elif op == 3:
        break


print("----------THANK YOU----------")