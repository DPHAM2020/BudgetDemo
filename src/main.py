import Account

def main():
    DanhAccount = Account.Account("Danh", 600.00)
    DanhAccount.new_category("savings", 0.3)
    DanhAccount.new_category("needs", 0.4)
    DanhAccount.redistribute_funds()
    DanhAccount.print_info()
    DanhAccount.deposit(50)
    DanhAccount.print_info()


if __name__ == '__main__':
    main()

