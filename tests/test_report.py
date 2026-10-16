from decimal import Decimal

from expenses import category_totals, monthly_totals, parse_csv

SAMPLE = """date,category,amount
2026-01-03,food,12.50
2026-01-15,rent,900.00
2026-02-01,food,8.25
"""


def test_category_totals():
    assert category_totals(parse_csv(SAMPLE)) == {
        "food": Decimal("20.75"),
        "rent": Decimal("900.00"),
    }


def test_monthly_totals_sum():
    totals = monthly_totals(parse_csv(SAMPLE))
    assert sum(totals.values()) == Decimal("920.75")
    assert len(totals) == 2
