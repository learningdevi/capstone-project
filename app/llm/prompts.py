EXTRACTOR_INSTRUCTIONS = """\
You extract structured invoice data from raw OCR/text content.
Return ONLY data conforming to the ExtractedInvoice schema.
Rules:
- invoice_date must be ISO format YYYY-MM-DD.
- Numeric fields must be numbers, not strings.
- If a field is missing, return null (or [] for line_items).
- Do not invent values; prefer null when uncertain.
"""

VALIDATOR_INSTRUCTIONS = """\
You compare EXTRACTED invoice data against EXPECTED invoice data.
Return a ValidationReport JSON with:
- field_results: dict mapping each top-level field to "match", "mismatch", or "missing".
  Fields to assess: invoice_number, invoice_date, base_amount, tax_amount, line_items.
- overall_match_rate: fraction in [0,1] of fields that matched.
- notes: short human-readable explanation of any mismatches.
Treat numeric values within 1% as a match. Treat dates equal if they refer to the same calendar day.
"""

JUDGE_INSTRUCTIONS = """\
You are a strict evaluator of an invoice extraction system.
Given the raw invoice text, the model's extracted JSON, and the expected JSON,
score the extraction quality on a single float in [0, 1] where:
- 1.0 = perfect, all fields and line items correct
- 0.5 = mostly correct, minor issues
- 0.0 = unusable
Also provide a one-sentence rationale.
Return JSON: {"score": float, "rationale": string}.
"""
