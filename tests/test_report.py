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


def test_monthly_totals_year_month_keys():
    # Test that same month in different years gives separate totals
    csv_data = """date,category,amount
2025-01-05,food,10
2026-01-05,food,5
"""
    totals = monthly_totals(parse_csv(csv_data))
    
    # Should have separate entries for 2025-01 and 2026-01
    assert "2025-01" in totals
    assert "2026-01" in totals
    assert totals["2025-01"] == Decimal("10")
    assert totals["2026-01"] == Decimal("5")
    
    # Should not have a bare month key like '01'
    assert "01" not in totals
