from datetime import date

# An instance of money spent on something
class Expense:
    def __init__(self, title: str, amount: float, date_of_expense: date, description: str = None):
        self.title = title
        self.amount = amount
        self.expense_date = date_of_expense
        self.description = description


    def __repr__(self):
        #print(self.title + " -- " + self.expense_date + " -- " + self.amount + " -- " + self.description)
        return f'{self.title} -- {self.expense_date} -- ${self.amount} -- {self.description}'