from datetime import datetime

from repository import (
    get_expense_by_id,
    get_expenses_by_month,
    get_totals_by_category,
    list_all_expenses,
)
from services import (
    add_expense,
    delete_expense,
    edit_expense,
    get_budget_status,
    maintain_budget,
)


def display_expense_table(rows) -> bool:
    if not rows:
        print("No expenses recorded yet")
        return False

    print("\n" + "=" * 55)
    print(f"{'id':<5} | {'Date':<10} | {'Amount':<10} | {'Category':<12} | {'Note'}")
    print("=" * 55)

    for expense_id, date, amount, category, note in rows:
        note_display = note if note else "-"
        print(
            f"{expense_id:<5} | {date:<10} | ${amount:<9.2f} | {category:<12} | {note_display}"
        )
    print("=" * 55)
    return True


def expense_id_input() -> int | None:
    value = input("Enter expense ID (or empty to cancel): ").strip()

    if value == "":
        return None

    if not value.isdigit():
        print("invalid ID , type a number!")
        return None

    return int(value)


def get_valid_amount(prompt="Amount : ") -> float:
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                raise ValueError
            return amount
        except ValueError:
            print("Amount must be a positive number!")


def get_valid_date(
    prompt="Date (YYYY-MM-DD) [empty = today]: ", allow_empty=True
) -> str:
    while True:
        date_input = input(prompt).strip()
        if not date_input and allow_empty:
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
            return date_input
        except ValueError:
            print("Invalid date format , use YYYY-MM-DD ")


def main_menu():
    while True:
        print("""
====== Personal Expense Tracker ======
1. Add expense
2. List expenses
3. Totals by category
4. Filter by month
5. Edit expense
6. Delete expense
7. Set category budget
8. View budget status
9. Exit
""")

        choice = input("Choose: ").strip()

        if choice == "1":
            print("\n ======= Adding new expense ====== ")
            amount = get_valid_amount()
            category = input("Category : ").strip().lower()
            date = get_valid_date()
            note = input("Note (optional): ").strip() or None

            add_expense(amount, category, date, note)
            print("\n Expense added successfuly!")

        elif choice == "2":
            rows = list_all_expenses()
            display_expense_table(rows)

        elif choice == "3":
            rows = get_totals_by_category()
            if not rows:
                print("No data.")
                continue

            print("\n====== Totals by Category =======")
            for category, total in rows:
                print(f"{category:<15} : ${total:.2f}")

        elif choice == "4":
            print("\n===== Filter Expenses by Month =====")
            year = input("Year (YYYY): ").strip()
            month = input("Month (MM): ").strip()

            if not (
                year.isdigit()
                and len(year) == 4
                and month.isdigit()
                and 1 <= int(month) <= 12
            ):
                print("Invalid month or year format.")
                continue

            period = f"{year}-{month.zfill(2)}"

            rows = get_expenses_by_month(period)
            if not rows:
                print(f"No expenses founf for {period}")
                continue

            total = 0
            print(f"\n===== Expenses for {period} =====")
            for date, amount, category in rows:
                print(f"{date} : ${amount:.2f} | {category}")
                total += amount

            print(f"Total spent in {period}: ${total:.2f}")

        elif choice == "5":
            print("\n======= Edit Expense =======")
            rows = list_all_expenses()

            if not display_expense_table(rows):
                continue

            expense_id = expense_id_input()
            if expense_id is None:
                continue

            amount = get_valid_amount("New amount : ")
            category = input("New category : ").strip().lower()
            date = get_valid_date("New date (YYYY-MM-DD): ", allow_empty=False)
            note = input("New note (optional): ").strip() or None

            if edit_expense(expense_id, amount, category, date, note):
                print("Expense updated successfuly ! ")
            else:
                print("Expense not found.")

        elif choice == "6":
            print("\n======= Delete Expense =======")
            rows = list_all_expenses()
            if not display_expense_table(rows):
                continue

            expense_id = expense_id_input()
            if expense_id is None:
                continue

            expense = get_expense_by_id(expense_id)
            if not expense:
                print("expense not found.")
                continue

            print(f"\nDelete ID {expense[0]} | ${expense[1]} | {expense[2]}?")
            delete_expense(expense_id)
            print("Expense deleted.")

        elif choice == "7":
            print("\n===== Set Category Budget =====")
            category = input("Category: ").strip().lower()
            if not category:
                print("Category cannot be empty.")
                continue
            limit = get_valid_amount("Monthly Limit ($): ")

            maintain_budget(category, limit)
            print(f"Budget for '{category}' saved.")

        elif choice == "8":
            report = get_budget_status()
            if not report:
                print("\nNo budget limits set yet.")
                continue

            print("\n" + "=" * 65)
            for item in report:
                status = (
                    f"🟢 ${item['remaining']:.2f} left"
                    if item["remaining"] >= 0
                    else f"🔴 Over by ${abs(item['remaining']):.2f}"
                )
                print(
                    f"{item['category']:<15} | Spent: ${item['spent']:<8.2f} | Limit: ${item['limit']:<8.2f} | {status}"
                )
                print("=" * 65)

        elif choice == "9":
            print("Quitting ... ")
            break
        else:
            print("Invalid choice.")
