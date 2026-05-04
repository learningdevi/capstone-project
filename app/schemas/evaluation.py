from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.invoice import ExtractedInvoice, ProcessResponse


class EvalCase(BaseModel):
    case_id: str
    pdf_path: str
    expected: ExtractedInvoice
    metadata: dict = Field(default_factory=dict)


class EvalCaseResult(BaseModel):
    case_id: str
    deterministic_score: float
    judge_score: float
    judge_rationale: str
    response: ProcessResponse


class EvalSummary(BaseModel):
    per_case: list[EvalCaseResult]
    avg_deterministic: float
    avg_judge: float
    avg_overall: float


class EvaluateRequest(BaseModel):
    dataset_path: str | None = None
    cases: list[EvalCase] | None = None
