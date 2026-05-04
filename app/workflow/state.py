from __future__ import annotations

from pydantic import BaseModel

from app.schemas.invoice import ExtractedInvoice, ValidationReport


class AgentState(BaseModel):
    pdf_path: str
    expected: ExtractedInvoice
    raw_text: str = ""
    extracted: ExtractedInvoice | None = None
    validation: ValidationReport | None = None
