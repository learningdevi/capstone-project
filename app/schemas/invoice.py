from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float


class ExtractedInvoice(BaseModel):
    invoice_number: str | None = None
    invoice_date: date | None = None
    base_amount: float | None = None
    tax_amount: float | None = None
    line_items: list[LineItem] = Field(default_factory=list)


class InvoiceRequest(BaseModel):
    metadata: dict = Field(default_factory=dict)
    pdf_path: str
    expected: ExtractedInvoice


FieldStatus = Literal["match", "mismatch", "missing"]


class ValidationReport(BaseModel):
    field_results: dict[str, FieldStatus]
    overall_match_rate: float
    notes: str = ""


class ProcessResponse(BaseModel):
    extracted: ExtractedInvoice
    validation: ValidationReport
