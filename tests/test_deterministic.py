from datetime import date

from app.evaluation.deterministic import deterministic_score
from app.schemas.invoice import ExtractedInvoice, LineItem


def test_perfect_match():
    inv = ExtractedInvoice(
        invoice_number="A1",
        invoice_date=date(2025, 1, 1),
        base_amount=100.0,
        tax_amount=18.0,
        line_items=[LineItem(description="x", quantity=1, unit_price=100, amount=100)],
    )
    assert deterministic_score(inv, inv) == 1.0


def test_partial_mismatch():
    a = ExtractedInvoice(invoice_number="A1", base_amount=100, tax_amount=18)
    b = ExtractedInvoice(invoice_number="A2", base_amount=100, tax_amount=18)
    score = deterministic_score(a, b)
    assert 0.0 < score < 1.0


def test_numeric_tolerance():
    a = ExtractedInvoice(base_amount=100.0, tax_amount=18.0)
    b = ExtractedInvoice(base_amount=100.005, tax_amount=18.0)
    # Within 1% tolerance for base_amount
    assert deterministic_score(a, b) > 0.0
