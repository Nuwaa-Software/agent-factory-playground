"""Parse expenses from CSV text with header: date,category,amount[,note]."""

import csv
import io
from datetime import date
from decimal import Decimal

from expenses.models import Expense


def parse_csv(text: str) -> list[Expense]:
    lines = [line for line in text.strip().splitlines() if line.strip()]
    if not lines:
        return []
    
    # Use csv.reader to properly handle quoted fields
    reader = csv.reader(io.StringIO(text))
    header = next(reader)
    if header[:3] != ["date", "category", "amount"]:
        raise ValueError(f"unexpected header: {header!r}")

    expenses = []
    for row in reader:
        # Handle empty rows
        if not row:
            continue
            
        note = row[3] if len(row) > 3 else ""
        # Strip thousands separators from amount before converting to Decimal
        amount_str = row[2].replace(",", "")
        expenses.append(
            Expense(
                date=date.fromisoformat(row[0]),
                category=row[1].lower(),
                amount=Decimal(amount_str),
                note=note,
            )
        )
    return expenses
