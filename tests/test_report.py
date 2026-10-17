from decimal import Decimal

from expenses import category_totals, monthly_totals, parse_csv, top_categories

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


def test_top_categories_normal():
    """Test normal case with 4 categories, n=3"""
    csv_data = """date,category,amount
2026-01-03,food,12.50
2026-01-15,rent,900.00
2026-02-01,food,8.25
2026-02-05,entertainment,50.00
2026-02-10,groceries,25.00
"""
    result = top_categories(parse_csv(csv_data), n=3)
    # Should return top 3 by total amount
    assert len(result) == 3
    assert result[0][0] == "rent"  # highest total (900.00)
    assert result[1][0] == "entertainment"  # second highest (50.00)
    assert result[2][0] == "groceries"  # third highest (25.00)


def test_top_categories_ties():
    """Test tie-breaking by alphabetical order"""
    csv_data = """date,category,amount
2026-01-03,food,10.00
2026-01-15,rent,10.00
2026-02-01,groceries,5.00
"""
    result = top_categories(parse_csv(csv_data), n=3)
    # food and rent both have 10.00, so food comes first alphabetically (before rent)
    assert len(result) == 3
    assert result[0][0] == "food"  # lower alphabetical order comes first
    assert result[1][0] == "rent"  # higher alphabetical order comes second
    assert result[2][0] == "groceries"


def test_top_categories_empty():
    """Test empty input returns empty list"""
    assert top_categories([]) == []


def test_top_categories_fewer_than_n():
    """Test when there are fewer categories than n"""
    csv_data = """date,category,amount
2026-01-03,food,12.50
2026-01-15,rent,900.00
"""
    result = top_categories(parse_csv(csv_data), n=5)
    # Should return both categories in descending order
    assert len(result) == 2
    assert result[0][0] == "rent"
    assert result[1][0] == "food"


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
