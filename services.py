from datetime import datetime

from repository import (
    delete_expense_by_id,
    get_all_budgets,
    get_expense_by_id,
    get_monthly_spending_by_category,
    insert_expense,
    set_budget,
    update_expense,
)


def add_expense(amount: float, category: str, date: str, note: str | None) -> None:
    insert_expense(amount, category, date, note)


def edit_expense(
    expense_id: int, amount: float, category: str, date: str, note: str | None
) -> bool:
    return update_expense(
        expense_id, amount=amount, category=category, date=date, note=note
    )


def delete_expense(expense_id: int) -> bool:
    expense = get_expense_by_id(expense_id)
    if expense is None:
        return False

    delete_expense_by_id(expense_id)
    return True


def maintain_budget(category: str, limit: float) -> None:
    set_budget(category, limit)


def get_budget_status() -> list[dict]:
    budgets = get_all_budgets()
    current_month = datetime.today().strftime("%Y-%m")
    spending_map = get_monthly_spending_by_category(current_month)

    status_report = []
    for category, limit in budgets:
        spent = spending_map.get(category, 0.0)
        status_report.append(
            {
                "category": category,
                "limit": limit,
                "spent": spent,
                "remaining": limit - spent,
            }
        )
    return status_report
