import json
from datetime import datetime
from json.decoder import JSONDecodeError

# Global list to store expenses in memory
EXPENSES = []


def load_data():
    global EXPENSES

    try:
        with open("expenses.json", "r") as file:
            EXPENSES = json.load(file)
            print(f"loaded {len(EXPENSES)} expenses from storage .")
    except FileNotFoundError:
        print("No previous data , new start .")
        EXPENSES = []
    except JSONDecodeError:
        print("data file was empty or corrupted. starting frash.")
        EXPENSES = []


def save_data():
    try:
        with open("expenses.json", "w") as file:
            json.dump(EXPENSES, file, indent=4)
            print("data saved !!")
    except Exception as e:
        print(f"Error saving data : {e}")


def add_expense():
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

    EXPENSES.append(expense)
    print(f"Expense of ${amount:.2f} in {category} added successfully")


def list_expenses():
    print("\n======= Your expenses =======")
    if not EXPENSES:
        print("\n no expenses recorded yet.")
        return
    else:
        for exp in EXPENSES:
            # amount = exp.get("amount", 0)
            # category = exp.get("category", "Unknown")
            # print(f"Amount: {amount} $, Category: {category}")
            print(f"Amount : {exp['amount']} $, Category : {exp['category']}")


def total_by_category():
    if not EXPENSES:
        print("no data to calculate")
        return

    totals = {}

    for exp in EXPENSES:
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
    while True:
        print("====== your Personal tracker ======")
        print("1. add expense")
        print("2. list all expenses")
        print("3. view category totals")
        print("4. Exit")

        choice = input("Choose an option(1 --> 4) : ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            total_by_category()
        elif choice == "4":
            print("saving data ....byye")
            save_data()
            break
        else:
            print("invalide choice , enter a number between 1 and 4")


if __name__ == "__main__":
    load_data()
    main_menu()
