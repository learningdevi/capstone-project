from fastapi import FastAPI

from app.api.routes_eval import router as eval_router
from app.api.routes_invoice import router as invoice_router

app = FastAPI(title="Invoice Processor", version="0.1.0")
app.include_router(invoice_router)
app.include_router(eval_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
