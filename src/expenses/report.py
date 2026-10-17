"""Aggregate expenses into simple reports."""

from collections import defaultdict
from decimal import Decimal

from expenses.models import Expense


def category_totals(expenses: list[Expense]) -> dict[str, Decimal]:
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for e in expenses:
        totals[e.category] += e.amount
    return dict(totals)


def top_categories(expenses: list[Expense], n: int = 3) -> list[tuple[str, Decimal]]:
    """Returns the n categories with the highest total, sorted from highest to lowest.
    
    Ties are broken alphabetically by category name.
    If there are fewer than n categories, returns all of them.
    Empty input returns [].
    """
    totals = category_totals(expenses)
    # Sort by (-total, category) so highest totals come first,
    # and ties are broken alphabetically
    sorted_items = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return sorted_items[:n]


def monthly_totals(expenses: list[Expense]) -> dict[str, Decimal]:
    """Total spent per month, keyed by 'YYYY-MM'."""
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for e in expenses:
        key = f"{e.date.year:04d}-{e.date.month:02d}"
        totals[key] += e.amount
    return dict(totals)
