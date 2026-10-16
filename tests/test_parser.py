from datetime import date
from decimal import Decimal

import pytest

from expenses import parse_csv

SAMPLE = """date,category,amount,note
2026-01-03,Food,12.50,lunch
2026-01-15,Rent,900.00,
2026-02-01,food,8.25
"""


def test_parses_rows():
    rows = parse_csv(SAMPLE)
    assert len(rows) == 3
    assert rows[0].date == date(2026, 1, 3)
    assert rows[0].amount == Decimal("12.50")
    assert rows[0].note == "lunch"


def test_category_is_lowercased():
    assert {r.category for r in parse_csv(SAMPLE)} == {"food", "rent"}


def test_empty_input():
    assert parse_csv("") == []


def test_bad_header():
    with pytest.raises(ValueError):
        parse_csv("when,what,how much\n2026-01-01,x,1")


def test_quoted_amount_with_thousands_separator():
    csv_text = """date,category,amount,note
2026-03-01,rent,"1,250.00",march rent
"""
    rows = parse_csv(csv_text)
    assert len(rows) == 1
    assert rows[0].amount == Decimal("1250.00")


def test_quoted_note_with_comma():
    csv_text = """date,category,amount,note
2026-03-02,food,9.99,"lunch, with team"
"""
    rows = parse_csv(csv_text)
    assert len(rows) == 1
    assert rows[0].note == "lunch, with team"
