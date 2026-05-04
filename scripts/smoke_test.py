"""End-to-end smoke test: run the full pipeline against a sample invoice."""
import asyncio
import json

from app.schemas.invoice import ExtractedInvoice, LineItem
from app.workflow.graph import run_pipeline
from app.workflow.state import AgentState


async def main() -> None:
    expected = ExtractedInvoice(
        invoice_number="INV-001",
        invoice_date="2025-01-15",  # type: ignore[arg-type]
        base_amount=1000.00,
        tax_amount=180.00,
        line_items=[
            LineItem(description="Consulting Services", quantity=10, unit_price=100.0, amount=1000.0)
        ],
    )
    state = AgentState(pdf_path="data/sample_invoices/invoice_001.pdf", expected=expected)
    final = await run_pipeline(state)

    print("\n=== RAW TEXT (first 300 chars) ===")
    print(final.raw_text[:300])
    print("\n=== EXTRACTED ===")
    print(json.dumps(final.extracted.model_dump(mode="json"), indent=2))  # type: ignore[union-attr]
    print("\n=== VALIDATION ===")
    print(json.dumps(final.validation.model_dump(mode="json"), indent=2))  # type: ignore[union-attr]


if __name__ == "__main__":
    asyncio.run(main())
