import pytest
from decimal import Decimal

from expenses import Expense, parse_csv, over_budget


def test_over_budget_over():
    """Test that categories over budget are returned with correct overage."""
    expenses = [
        Expense(date="2023-01-01", category="food", amount=Decimal("50.00")),
        Expense(date="2023-01-02", category="food", amount=Decimal("30.00")),
    ]
    budgets = {"food": Decimal("70.00")}
    
    result = over_budget(expenses, budgets)
    assert result == {"food": Decimal("10.00")}


def test_over_budget_equal():
    """Test that categories exactly at budget are not included."""
    expenses = [
        Expense(date="2023-01-01", category="food", amount=Decimal("50.00")),
        Expense(date="2023-01-02", category="food", amount=Decimal("50.00")),
    ]
    budgets = {"food": Decimal("100.00")}
    
    result = over_budget(expenses, budgets)
    assert result == {}


def test_over_budget_under():
    """Test that categories under budget are not included."""
    expenses = [
        Expense(date="2023-01-01", category="food", amount=Decimal("50.00")),
        Expense(date="2023-01-02", category="food", amount=Decimal("30.00")),
    ]
    budgets = {"food": Decimal("100.00")}
    
    result = over_budget(expenses, budgets)
    assert result == {}


def test_over_budget_case_insensitive():
    """Test case-insensitive matching between budget keys and expense categories."""
    expenses = [
        Expense(date="2023-01-01", category="food", amount=Decimal("50.00")),
    ]
    budgets = {"Food": Decimal("40.00")}  # Capital F
    
    result = over_budget(expenses, budgets)
    assert result == {"Food": Decimal("10.00")}


def test_over_budget_multiple_categories():
    """Test mix of over, equal, and under budget categories."""
    expenses = [
        Expense(date="2023-01-01", category="food", amount=Decimal("60.00")),
        Expense(date="2023-01-02", category="food", amount=Decimal("20.00")),  # 80 total
        Expense(date="2023-01-03", category="transport", amount=Decimal("30.00")),
        Expense(date="2023-01-04", category="transport", amount=Decimal("70.00")),  # 100 total
        Expense(date="2023-01-05", category="entertainment", amount=Decimal("50.00")),
    ]
    budgets = {
        "food": Decimal("75.00"),      # 80 > 75 → over by 5
        "transport": Decimal("100.00"), # 100 == 100 → equal
        "entertainment": Decimal("40.00"), # 50 > 40 → over by 10
        "unknown": Decimal("10.00"),   # not in expenses → ignored
    }
    
    result = over_budget(expenses, budgets)
    assert result == {"food": Decimal("5.00"), "entertainment": Decimal("10.00")}


def test_over_budget_unknown_expense_categories():
    """Test that expense categories not in budgets are ignored."""
    expenses = [
        Expense(date="2023-01-01", category="food", amount=Decimal("50.00")),
        Expense(date="2023-01-02", category="unknown_category", amount=Decimal("30.00")),
    ]
    budgets = {"food": Decimal("40.00")}
    
    result = over_budget(expenses, budgets)
    assert result == {"food": Decimal("10.00")}


def test_over_budget_empty_inputs():
    """Test with empty expenses and budgets."""
    result = over_budget([], {})
    assert result == {}


def test_over_budget_empty_expenses():
    """Test with empty expenses list."""
    budgets = {"food": Decimal("100.00")}
    result = over_budget([], budgets)
    assert result == {}


def test_over_budget_empty_budgets():
    """Test with empty budgets dict."""
    expenses = [
        Expense(date="2023-01-01", category="food", amount=Decimal("50.00")),
    ]
    result = over_budget(expenses, {})
    assert result == {}