import json
from datetime import datetime

# Global list to store expenses in memory


def load_data():

    try:
        with open("expenses.json", "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []  # Returns an empty list if no file exists


def save_data(expense_list):
    with open("expenses.json", "w") as file:
        json.dump(expense_list, file, indent=4)


def add_expense(current_expenses):
    print("\n======= Add new expense =======")

    while True:
        try:
            amount = float(input("Amount : "))
            if amount <= 0:
                print("amount must be positive.")
                continue
            break
        except ValueError:
            print("Invalide input . enter a valid number(eg. 40.50)")

    category = input("Category (eg. food , transport) :").strip().capitalize()

    date_input = input("Date(YYYY-MM-DD) [leave blank for today]: ").strip()
    if not date_input:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        date = date_input

    note = input("Note , description : ").strip()

    expense = {"amount": amount, "category": category, "date": date, "note": note}

    current_expenses.append(expense)
    save_data(current_expenses)
    print(f"Expense of ${amount:.2f} in {category} added successfully")


def list_expenses(my_expenses):
    print("\n======= Your expenses =======")
    if not my_expenses:
        print("\n no expenses recorded yet.")
        return
    else:
        for exp in my_expenses:
            amount = exp.get("amount", 0)
            category = exp.get("category", "Unknown")
            print(f"Amount: {amount} $, Category: {category}")


def filter_by_month(month_expenses):
    if not month_expenses:
        print("\n no expenses recorded yet.")
        return

    print("=======\n Filter Expenses by month ========")
    year = input("Enter year (eg. 2026)").strip()
    month = input("Enter month (eg. 06").strip()

    period = f"{year}-{month}"
    print(f"\nShowing expenses for {period} :")
    print("-" * 50)

    found = False
    total_for_month = 0.0

    for exp in month_expenses:
        if exp["date"].startswith(period):
            print(f"Amount: {exp['amount']} $ , Category : {exp['category']}")
            total_for_month += exp["amount"]
            found = True

    if not found:
        print("No expenses found for this period.")
    else:
        print("-" * 50)
        print(f"Total spending for {period}: {total_for_month:.2f}")


def total_by_category(category_expenses):
    if not category_expenses:
        print("\n no expenses recorded yet.")
        return

    totals = {}

    for exp in category_expenses:
        cat = exp["category"]
        amt = exp["amount"]

        if cat in totals:
            totals[cat] += amt
        else:
            totals[cat] = amt

    print("\n ======= Spending by category =======")
    for cat, total in totals.items():
        print(f"{cat}: ${total:.2f}")


def main_menu():
    my_expenses = load_data()

    while True:
        print("====== your Personal tracker ======")
        print("1. add expense")
        print("2. list all expenses")
        print("3. view category totals")
        print("4. filter expenses by month")
        print("5. Exit")

        choice = input("Choose an option(1 --> 5) : ").strip()

        if choice == "1":
            add_expense(my_expenses)
            save_data(my_expenses)
        elif choice == "2":
            list_expenses(my_expenses)
        elif choice == "3":
            total_by_category(my_expenses)
        elif choice == "4":
            filter_by_month(my_expenses)
        elif choice == "5":
            print("saving data ....byye")
            save_data(my_expenses)
            break
        else:
            print("invalide choice , enter a number between 1 and 5")


if __name__ == "__main__":
    main_menu()
