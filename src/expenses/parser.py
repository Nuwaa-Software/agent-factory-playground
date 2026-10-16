"""Parse expenses from CSV text with header: date,category,amount[,note]."""

from datetime import date
from decimal import Decimal

from expenses.models import Expense


def parse_csv(text: str) -> list[Expense]:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return []
    header = [h.strip().lower() for h in lines[0].split(",")]
    if header[:3] != ["date", "category", "amount"]:
        raise ValueError(f"unexpected header: {lines[0]!r}")

    expenses = []
    for line in lines[1:]:
        fields = [f.strip() for f in line.split(",")]
        note = fields[3] if len(fields) > 3 else ""
        expenses.append(
            Expense(
                date=date.fromisoformat(fields[0]),
                category=fields[1].lower(),
                amount=Decimal(fields[2]),
                note=note,
            )
        )
    return expenses
