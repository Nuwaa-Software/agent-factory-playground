"""Aggregate expenses into simple reports."""

from collections import defaultdict
from decimal import Decimal

from expenses.models import Expense


def category_totals(expenses: list[Expense]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for e in expenses:
        totals[e.category] += e.amount
    return dict(totals)


def monthly_totals(expenses: list[Expense]) -> dict[str, Decimal]:
    """Total spent per month, keyed by 'YYYY-MM'."""
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for e in expenses:
        key = f"{e.date.year:04d}-{e.date.month:02d}"
        totals[key] += e.amount
    return dict(totals)
