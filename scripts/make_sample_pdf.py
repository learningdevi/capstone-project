"""Generate a sample invoice PDF for end-to-end testing."""
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

OUT = Path(__file__).resolve().parent.parent / "data" / "sample_invoices" / "invoice_001.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

c = canvas.Canvas(str(OUT), pagesize=LETTER)
w, h = LETTER
y = h - 60

c.setFont("Helvetica-Bold", 18)
c.drawString(50, y, "ACME CORP")
y -= 20
c.setFont("Helvetica", 10)
c.drawString(50, y, "123 Main St, Springfield")
y -= 30

c.setFont("Helvetica-Bold", 14)
c.drawString(50, y, "INVOICE")
y -= 25

c.setFont("Helvetica", 11)
c.drawString(50, y, "Invoice Number: INV-001")
y -= 16
c.drawString(50, y, "Invoice Date: 2025-01-15")
y -= 16
c.drawString(50, y, "Bill To: Globex Inc.")
y -= 30

c.setFont("Helvetica-Bold", 11)
c.drawString(50, y, "Description")
c.drawString(280, y, "Qty")
c.drawString(340, y, "Unit Price")
c.drawString(440, y, "Amount")
y -= 14
c.line(50, y, 540, y)
y -= 16

c.setFont("Helvetica", 11)
items = [
    ("Consulting Services",   10, 100.00, 1000.00),
]
for desc, qty, unit, amt in items:
    c.drawString(50, y, desc)
    c.drawString(280, y, f"{qty}")
    c.drawString(340, y, f"${unit:,.2f}")
    c.drawString(440, y, f"${amt:,.2f}")
    y -= 16

y -= 10
c.line(50, y, 540, y)
y -= 18
c.setFont("Helvetica", 11)
c.drawString(340, y, "Base Amount:")
c.drawString(440, y, "$1,000.00")
y -= 16
c.drawString(340, y, "Tax (18%):")
c.drawString(440, y, "$180.00")
y -= 16
c.setFont("Helvetica-Bold", 11)
c.drawString(340, y, "Total:")
c.drawString(440, y, "$1,180.00")

c.showPage()
c.save()
print(f"Wrote {OUT}")
