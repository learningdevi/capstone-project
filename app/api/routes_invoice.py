from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.schemas.invoice import InvoiceRequest, ProcessResponse
from app.workflow.graph import run_pipeline
from app.workflow.state import AgentState

router = APIRouter(prefix="/api", tags=["invoice"])


@router.post("/process_invoice", response_model=ProcessResponse)
async def process_invoice(req: InvoiceRequest) -> ProcessResponse:
    if not Path(req.pdf_path).is_file():
        raise HTTPException(status_code=400, detail=f"PDF not found: {req.pdf_path}")
    state = AgentState(pdf_path=req.pdf_path, expected=req.expected)
    final = await run_pipeline(state)
    if not final.extracted or not final.validation:
        raise HTTPException(status_code=500, detail="Pipeline did not produce a complete result")
    return ProcessResponse(extracted=final.extracted, validation=final.validation)
