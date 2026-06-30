from db import get_connection


def set_budget(category: str, limit: float) -> None:
    conn, cursor = get_connection()

    cursor.execute(
        """
        INSERT INTO budgets (category, monthly_limit)
        VALUES (?,?)
        ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit
        """,
        (category, limit),
    )
    conn.commit()
    conn.close()


def get_all_budgets() -> list[tuple]:
    conn, cursor = get_connection()
    cursor.execute("SELECT category, monthly_limit FROM budgets ORDER BY category ASC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_monthly_spending_by_category(period: str) -> dict[str, float]:
    conn, cursor = get_connection()
    cursor.execute(
        """
        SELECT category, SUM(amount)
        FROM expenses
        WHERE date LIKE ?
        GROUP BY category
        """,
        (f"{period}%",),
    )

    rows = cursor.fetchall()
    conn.close()
    return {category: total for category, total in rows}


def insert_expense(
    amount: float,
    category: str,
    date: str,
    note: str | None,
) -> None:
    conn, cursor = get_connection()

    cursor.execute(
        """
        INSERT INTO expenses (amount, category, date, note)
        VALUES (?,?,?,?)
        """,
        (amount, category, date, note),
    )
    conn.commit()
    conn.close()


def list_all_expenses():
    conn, cursor = get_connection()
    cursor.execute(
        "SELECT id, date, amount, category, note FROM expenses ORDER BY date DESC"
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expense_by_id(expense_id: int) -> tuple | None:
    conn, cursor = get_connection()

    cursor.execute(
        """
        SELECT id, amount, category, date, note
        FROM expenses
        WHERE id = ?
        """,
        (expense_id,),
    )

    row = cursor.fetchone()
    conn.close()
    return row


def update_expense(
    expense_id: int, *, amount: float, category: str, date: str, note: str | None
) -> bool:
    conn, cursor = get_connection()

    cursor.execute(
        """
        UPDATE expenses
        SET amount = ?, category = ?, date = ?, note = ?
        WHERE id = ?
        """,
        (amount, category, date, note, expense_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()

    return updated


def delete_expense_by_id(expense_id: int) -> None:
    conn, cursor = get_connection()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()


def get_totals_by_category() -> list[tuple]:
    conn, cursor = get_connection()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expenses_by_month(period: str) -> list[tuple]:
    conn, cursor = get_connection()
    cursor.execute(
        """
        SELECT date, amount, category
        FROM expenses
        WHERE date LIKE ?
        """,
        (f"%{period}%",),
    )

    rows = cursor.fetchall()
    conn.close()
    return rows
