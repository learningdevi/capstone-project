from fastapi import APIRouter, HTTPException

from app.evaluation.runner import evaluate, load_cases
from app.schemas.evaluation import EvalSummary, EvaluateRequest

router = APIRouter(prefix="/api", tags=["evaluation"])


@router.post("/evaluate", response_model=EvalSummary)
async def run_evaluation(req: EvaluateRequest) -> EvalSummary:
    if not req.cases and not req.dataset_path:
        raise HTTPException(status_code=400, detail="Provide either 'cases' or 'dataset_path'")
    cases = req.cases or load_cases(req.dataset_path)  # type: ignore[arg-type]
    if not cases:
        raise HTTPException(status_code=400, detail="No evaluation cases found")
    return await evaluate(cases)
