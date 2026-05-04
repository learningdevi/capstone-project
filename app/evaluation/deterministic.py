from __future__ import annotations

import math

from app.schemas.invoice import ExtractedInvoice, LineItem


def _num_close(a: float | None, b: float | None) -> bool:
    if a is None or b is None:
        return a == b
    return math.isclose(a, b, rel_tol=1e-2, abs_tol=1e-2)


def _line_items_equal(a: list[LineItem], b: list[LineItem]) -> bool:
    if len(a) != len(b):
        return False
    sa = sorted(a, key=lambda i: i.description.strip().lower())
    sb = sorted(b, key=lambda i: i.description.strip().lower())
    for x, y in zip(sa, sb):
        if x.description.strip().lower() != y.description.strip().lower():
            return False
        if not (
            _num_close(x.quantity, y.quantity)
            and _num_close(x.unit_price, y.unit_price)
            and _num_close(x.amount, y.amount)
        ):
            return False
    return True


def deterministic_score(extracted: ExtractedInvoice, expected: ExtractedInvoice) -> float:
    checks = {
        "invoice_number": (extracted.invoice_number or "").strip()
        == (expected.invoice_number or "").strip(),
        "invoice_date": extracted.invoice_date == expected.invoice_date,
        "base_amount": _num_close(extracted.base_amount, expected.base_amount),
        "tax_amount": _num_close(extracted.tax_amount, expected.tax_amount),
        "line_items": _line_items_equal(extracted.line_items, expected.line_items),
    }
    return sum(checks.values()) / len(checks)
