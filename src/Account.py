
class Account:
    # Create an account for a user, setting up default values
    def __init__(self, username: str, starting_amount: float):
        self.user = username
        self.unallocated = starting_amount
        self.categories = {}                 # Category: ratio
        self.categories_balances = {}        # Category: balance


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
    

    def print_info(self):
        print("Hi " + self.user + ", your total balance is: " + str(round(self.unallocated, 2)))
        if not self.categories_balances:
            print("You have not set up your categories yet.")
        for category, balance in self.categories_balances.items():
            print("You have $" + str(balance) + " in " + category + ".")