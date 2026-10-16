from decimal import Decimal
from typing import List, Dict

from expenses.models import Expense


def over_budget(expenses: List[Expense], budgets: Dict[str, Decimal]) -> Dict[str, Decimal]:
    """
    Returns, for each category whose total spending is greater than its budget,
    how much it is over.
    
    Only categories present in `budgets` are checked.
    Category matching is case-insensitive.
    Spending exactly equal to the budget is not considered over budget.
    Uses Decimal for all arithmetic.
    """
    # Aggregate spending by category (already lowercase from parser)
    spending_by_category: Dict[str, Decimal] = {}
    
    for expense in expenses:
        category = expense.category
        if category in spending_by_category:
            spending_by_category[category] += expense.amount
        else:
            spending_by_category[category] = expense.amount
    
    # Check which categories are over budget
    result: Dict[str, Decimal] = {}
    
    for budget_category, budget_amount in budgets.items():
        # Case-insensitive matching: compare lowercase budget keys with expense categories
        for expense_category, spending in spending_by_category.items():
            if expense_category.lower() == budget_category.lower():
                if spending > budget_amount:
                    result[budget_category] = spending - budget_amount
    
    return result