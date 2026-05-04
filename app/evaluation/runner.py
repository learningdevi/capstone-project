from __future__ import annotations

import asyncio
import json
from pathlib import Path

from app.evaluation.deterministic import deterministic_score
from app.evaluation.judge import judge_score
from app.schemas.evaluation import EvalCase, EvalCaseResult, EvalSummary
from app.schemas.invoice import ProcessResponse
from app.workflow.graph import run_pipeline
from app.workflow.state import AgentState


def load_cases(path: str) -> list[EvalCase]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [EvalCase.model_validate(c) for c in data]


async def _run_one(case: EvalCase) -> EvalCaseResult:
    state = AgentState(pdf_path=case.pdf_path, expected=case.expected)
    final = await run_pipeline(state)
    assert final.extracted and final.validation
    det = deterministic_score(final.extracted, case.expected)
    verdict = await judge_score(final.raw_text, final.extracted, case.expected)
    return EvalCaseResult(
        case_id=case.case_id,
        deterministic_score=det,
        judge_score=verdict.score,
        judge_rationale=verdict.rationale,
        response=ProcessResponse(extracted=final.extracted, validation=final.validation),
    )


async def evaluate(cases: list[EvalCase], concurrency: int = 4) -> EvalSummary:
    sem = asyncio.Semaphore(concurrency)

    async def guarded(c: EvalCase) -> EvalCaseResult:
        async with sem:
            return await _run_one(c)

    results = await asyncio.gather(*(guarded(c) for c in cases))
    n = max(len(results), 1)
    avg_det = sum(r.deterministic_score for r in results) / n
    avg_judge = sum(r.judge_score for r in results) / n
    return EvalSummary(
        per_case=results,
        avg_deterministic=avg_det,
        avg_judge=avg_judge,
        avg_overall=(avg_det + avg_judge) / 2,
    )
