import Account


def main():
    DanhAccount = Account.Account("Danh", 600.00)
    DanhAccount.new_category("savings", 0.3)
    DanhAccount.new_category("needs", 0.4)
    DanhAccount.redistribute_funds()
    print(DanhAccount)
    DanhAccount.deposit(50)
    print(DanhAccount)
    res = DanhAccount.add_expense("gas", 60.00, 18, 4, 2025, "needs", "costco gas after work")
    if res == 1:
        print("There was an error adding the expense; no such category was found.")
    print(DanhAccount)


if __name__ == '__main__':
    main()

