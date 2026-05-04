from app.agents.judge import JudgeVerdict, build_judge_agent
from app.schemas.invoice import ExtractedInvoice
from app.workflow.graph import _coerce

_judge = None


def _get_judge():
    global _judge
    if _judge is None:
        _judge = build_judge_agent()
    return _judge


async def judge_score(
    raw_text: str, extracted: ExtractedInvoice, expected: ExtractedInvoice
) -> JudgeVerdict:
    prompt = (
        f"RAW_TEXT:\n{raw_text[:4000]}\n\n"
        f"EXTRACTED:\n{extracted.model_dump_json()}\n\n"
        f"EXPECTED:\n{expected.model_dump_json()}"
    )
    result = await _get_judge().run(prompt)
    return _coerce(JudgeVerdict, result)
