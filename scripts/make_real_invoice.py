"""Generate a realistic multi-line-item invoice PDF for end-to-end testing."""
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent.parent / "data" / "sample_invoices" / "invoice_real.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

# --- Invoice data (also used as ground truth in smoke_test_real.py) ---
INVOICE_NUMBER = "INV-2026-0042"
INVOICE_DATE = "2026-03-18"
VENDOR = "Northwind Technologies, Inc."
VENDOR_ADDR = "500 Market St, Suite 1200, Seattle, WA 98101"
BILL_TO = "Contoso Ltd. — Accounts Payable, 1 Microsoft Way, Redmond, WA 98052"

LINE_ITEMS = [
    ("Cloud Architecture Consulting",      20, 175.00),
    ("Azure OpenAI Implementation",        15, 200.00),
    ("Security Audit & Compliance Review",  8, 250.00),
    ("Knowledge Transfer Workshop",         4, 300.00),
]

TAX_RATE = 0.0875  # 8.75%

base_amount = round(sum(qty * unit for _, qty, unit in LINE_ITEMS), 2)
tax_amount = round(base_amount * TAX_RATE, 2)
total = round(base_amount + tax_amount, 2)

c = canvas.Canvas(str(OUT), pagesize=LETTER)
W, H = LETTER
y = H - 60

# Header
c.setFont("Helvetica-Bold", 22)
c.drawString(50, y, VENDOR)
y -= 18
c.setFont("Helvetica", 10)
c.drawString(50, y, VENDOR_ADDR)
y -= 14
c.drawString(50, y, "billing@northwind.example  |  +1 (206) 555-0142")
y -= 30

c.setFont("Helvetica-Bold", 20)
c.drawRightString(W - 50, y + 14, "INVOICE")

# Meta
c.setFont("Helvetica", 11)
c.drawString(50, y, f"Invoice Number: {INVOICE_NUMBER}")
y -= 16
c.drawString(50, y, f"Invoice Date: {INVOICE_DATE}")
y -= 16
c.drawString(50, y, f"Due Date: 2026-04-17")
y -= 24
c.setFont("Helvetica-Bold", 11)
c.drawString(50, y, "Bill To:")
c.setFont("Helvetica", 11)
y -= 14
c.drawString(50, y, BILL_TO)
y -= 30

# Table header
c.setFont("Helvetica-Bold", 11)
c.drawString(50, y, "Description")
c.drawString(330, y, "Qty")
c.drawString(380, y, "Unit Price")
c.drawString(490, y, "Amount")
y -= 6
c.line(50, y, W - 50, y)
y -= 16

# Rows
c.setFont("Helvetica", 11)
for desc, qty, unit in LINE_ITEMS:
    amount = round(qty * unit, 2)
    c.drawString(50, y, desc)
    c.drawString(330, y, f"{qty}")
    c.drawString(380, y, f"${unit:,.2f}")
    c.drawString(490, y, f"${amount:,.2f}")
    y -= 16

y -= 6
c.line(50, y, W - 50, y)
y -= 18

# Totals
c.setFont("Helvetica", 11)
c.drawString(380, y, "Base Amount:")
c.drawString(490, y, f"${base_amount:,.2f}")
y -= 16
c.drawString(380, y, f"Tax ({TAX_RATE*100:g}%):")
c.drawString(490, y, f"${tax_amount:,.2f}")
y -= 16
c.setFont("Helvetica-Bold", 11)
c.drawString(380, y, "Total Due:")
c.drawString(490, y, f"${total:,.2f}")

# Footer
y -= 50
c.setFont("Helvetica-Oblique", 9)
c.drawString(50, y, "Payment terms: Net 30. Please reference the invoice number on remittance.")

c.showPage()
c.save()
print(f"Wrote {OUT}")
print(f"Base: {base_amount}, Tax: {tax_amount}, Total: {total}")
