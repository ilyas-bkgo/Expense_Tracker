import sqlite3
from datetime import datetime

connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        date TEXT NOT NULL,
        note TEXT
    )
    """)
connection.commit()


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

    while True:
        date_input = input("Date(YYYY-MM-DD) [leave blank for today]: ").strip()
        if not date_input:
            date = datetime.today().strftime("%Y-%m-%d")
            break

        try:
            valid_date = datetime.strptime(date_input, "%Y-%m-%d")
            date = valid_date.strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD (e.g., 2026-06-21).")



    note = input("Note , description : ").strip()

    cursor.execute(
        """
        INSERT INTO expenses (amount, category, date, note)
        VALUES (?,?,?,?)
        """,
        (amount, category, date, note),
    )

    connection.commit()  # flushing changes into memory
    print(f"Expense of ${amount:.2f} in {category} added successfully")


def list_expenses():
    print("\n======= Your expenses =======")

    cursor.execute("SELECT amount, category FROM expenses")
    rows = cursor.fetchall()

    if not rows:
        print("\n No expenses recorded yet!")
        return

    for amount, category in rows:
        print(f"Amount: {amount}, Category: {category}")


def filter_by_month():

    print("=======\n Filter Expenses by month ========\n")
    year = input("Enter year (eg. 2026)").strip()
    month = input("Enter month (eg. 06)").strip()

    period = f"{year}-{month}"

    # We append the '%' inside the parameter tuple to stay safe from SQL Injection
    cursor.execute(
        """
        SELECT amount, category, date
        FROM expenses
        WHERE date LIKE ?
        """,
        (f"{period}%",),
    )

    rows = cursor.fetchall()

    if not rows:
        print(f"No expenses found for {period}")
        return

    print(f"\nShowing expenses for {period} :")
    print("-" * 50)

    total_for_month = 0.0

    for amount, category, date in rows:
        print(f"Date: {date} $ ,Amount: {amount} Category : {category}")
        total_for_month += amount

    print("-" * 50)
    print(f"Total spending for {period}: {total_for_month:.2f}")


def total_by_category():
    # aggregate the amount per category
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()

    if not rows:
        print("\n No data to calculate .")
        return

    print("\n ======= Spending by category =======\n")

    for category, total in rows:
        print(f"{category}: ${total:.2f}")


def main_menu():

    while True:
        print("\n====== your Personal tracker ======")
        print("1. add expense")
        print("2. list all expenses")
        print("3. view category totals")
        print("4. filter expenses by month")
        print("5. Exit")

        choice = input("\nChoose an option(1 --> 4) : ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            list_expenses()
        elif choice == "3":
            total_by_category()
        elif choice == "4":
            filter_by_month()
        elif choice == "5":
            print("\nClosing database connection....byye")
            connection.close()
            break
        else:
            print("invalide choice , enter a number between 1 and 4")


if __name__ == "__main__":
    main_menu()
