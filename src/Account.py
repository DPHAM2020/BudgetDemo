import Expense
from datetime import date

# General user account
class Account:
    # Create an account for a user, setting up default values
    def __init__(self, username: str, starting_amount: float):
        self.user = username
        self.unallocated = starting_amount
        self.categories = {}                 # Category: ratio
        self.categories_balances = {}        # Category: balance
        self.expenses = {}                   # title: Expense
        self.dates_to_expenses = {}          # date: Expense


    # Check that the sum of the ratios add up to 1 or less (can also account for a newly added ratio)
    def check_ratios(self, new_ratio=0.0) -> int:
        ratio_sum = sum(self.categories.values()) + new_ratio
        if ratio_sum > 1:
            return 1
        return 0


    # Create a new category 
    def new_category(self, category: str, ratio: float, redistribute: bool = False) -> int:
        if self.check_ratios(ratio) == 1:
            return 1
        
        self.categories[category] = ratio
        self.categories_balances[category] = 0

        if not redistribute:
            self.categories_balances[category] = 0
        else:
            if self.redistribute_funds() == 1:
                return 1
            
        return 0

    # Accumulate funds in all categories and unallocated funds, then redistribute funds based on ratios
    def redistribute_funds(self) -> int:
        sum_of_balances = sum(self.categories_balances.values()) + self.unallocated

        for category, ratio in self.categories.items():
            self.categories_balances[category] = sum_of_balances * ratio
        new_sum_of_balances = sum(self.categories_balances.values())
        self.unallocated = sum_of_balances - new_sum_of_balances

        return 0


    # Deposit money, automatically splitting between categories, if no categories set, then add to unallocated
    def deposit(self, amount: float) -> int:
        if not self.categories:
            self.unallocated += amount
            return 0
        
        amount_left = amount
        for category, ratio in self.categories.items():
            amount_to_add = round(amount * ratio, 2)
            amount_left -= amount_to_add

            self.categories_balances[category] += amount_to_add
            
        self.unallocated += amount_left

        return 0


    # Deposit money into a certain category
    def deposit_category(self, amount: float, category: str) -> int:
        if category in self.categories:
            self.categories_balances[category] += amount
            return 0
        else:
            return 1
    

        # 
    
    
    # Add an expense to the account
    def add_expense(self, title, amount: float, day, month, year, category=None, description = None) -> int:
        # TODO probably have to change this, because you can have same expense, 
        # but maybe different amount or different day, or update a previous expense 
        if title in self.expenses.keys():
            return 1
        
        # Subtract expense from appropriate balance
        category = category.lower()
        category_used = None
        if not category:
            self.unallocated -= amount
            category_used = self.unallocated
        elif category in self.categories.keys():
            self.categories_balances[category] -= amount
            category_used = self.categories_balances[category]
        else:
            return 1

        # Warn users about negative balance if the new expense puts one of their balances below zero 
        if category_used < 0.0:
            self.alert_negative_balance()

        # Create new expense object and add to list of expenses
        expense_date = date(year, month, day)
        new_expense = Expense.Expense(title, amount, expense_date, description)
        self.expenses[title] = new_expense
        self.dates_to_expenses[date] = new_expense
        return 0
    
    def alert_negative_balance(self):
        print("Warning! One or more balances has just went negative!")


    def __repr__(self):
        '''print('Hi ' + self.user + ', your total balance is: ' + str(round(self.unallocated, 2)))
        if not self.categories_balances:
            print('You have not set up your categories yet.')
        for category, balance in self.categories_balances.items():
            print('You have $' + str(balance) + ' in ' + category + '.')
        date_sorted_expenses = sorted(self.dates_to_expenses.items())
        print()'''
        return_str = [f'Hi {self.user}, your total balance is: {round(self.unallocated, 2)}. \n']

        return_str.append('You have: ')
        category_list = list(self.categories_balances.items())
        for i in range(len(category_list)):
            category, balance = category_list[i]
            if i == len(category_list)-1:
                return_str.append(f'and ${str(balance)} in {category}.\n')
                break
            return_str.append(f'${str(balance)} in {category}, ')

        return_str.append('Your category ratios are: ')
        ratio_list = list(self.categories.items())
        for i in range(len(category_list)):
            category, ratio = ratio_list[i]
            return_str.append(f'{ratio*100}% in {category}, ')
        unallocated_ratio = 1 - sum(self.categories.values())
        return_str.append(f'with {round(unallocated_ratio*100, 2)}% unallocated. \n')

        return_str.append('Expenses: \n')
        for _, expense in self.expenses.items():
            return_str.append(f'  >> {expense}\n')

        return ''.join(return_str)

