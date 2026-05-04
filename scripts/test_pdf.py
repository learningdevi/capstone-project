"""Run the pipeline on an arbitrary PDF (not necessarily a real invoice).

Usage: python scripts/test_pdf.py <pdf_path>
"""
import asyncio
import json
import sys
from pathlib import Path

from app.schemas.invoice import ExtractedInvoice
from app.workflow.graph import run_pipeline
from app.workflow.state import AgentState


async def main(pdf_path: str) -> None:
    if not Path(pdf_path).is_file():
        raise SystemExit(f"PDF not found: {pdf_path}")

    # No ground truth supplied; pass an empty ExtractedInvoice so validation
    # still runs and shows what mismatches the LLM detects.
    expected = ExtractedInvoice()
    state = AgentState(pdf_path=pdf_path, expected=expected)
    final = await run_pipeline(state)

    print("\n=== RAW TEXT (first 500 chars) ===")
    print(final.raw_text[:500])
    print("\n=== EXTRACTED ===")
    print(json.dumps(final.extracted.model_dump(mode="json"), indent=2))  # type: ignore[union-attr]
    print("\n=== VALIDATION ===")
    print(json.dumps(final.validation.model_dump(mode="json"), indent=2))  # type: ignore[union-attr]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python scripts/test_pdf.py <pdf_path>")
    asyncio.run(main(sys.argv[1]))
