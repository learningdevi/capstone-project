"""End-to-end test against a realistic multi-line-item invoice PDF."""
import asyncio
import json

from app.schemas.invoice import ExtractedInvoice, LineItem
from app.workflow.graph import run_pipeline
from app.workflow.state import AgentState

# Ground truth — kept in sync with scripts/make_real_invoice.py
EXPECTED = ExtractedInvoice(
    invoice_number="INV-2026-0042",
    invoice_date="2026-03-18",  # type: ignore[arg-type]
    base_amount=9700.00,
    tax_amount=848.75,
    line_items=[
        LineItem(description="Cloud Architecture Consulting",      quantity=20, unit_price=175.00, amount=3500.00),
        LineItem(description="Azure OpenAI Implementation",        quantity=15, unit_price=200.00, amount=3000.00),
        LineItem(description="Security Audit & Compliance Review", quantity=8,  unit_price=250.00, amount=2000.00),
        LineItem(description="Knowledge Transfer Workshop",        quantity=4,  unit_price=300.00, amount=1200.00),
    ],
)


async def main() -> None:
    state = AgentState(pdf_path="data/sample_invoices/invoice_real.pdf", expected=EXPECTED)
    final = await run_pipeline(state)

    print("\n=== EXTRACTED ===")
    print(json.dumps(final.extracted.model_dump(mode="json"), indent=2))  # type: ignore[union-attr]
    print("\n=== VALIDATION ===")
    print(json.dumps(final.validation.model_dump(mode="json"), indent=2))  # type: ignore[union-attr]


if __name__ == "__main__":
    asyncio.run(main())
