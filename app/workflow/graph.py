"""Linear 3-step pipeline implemented directly with async functions.

The use case calls for a graph workflow where shared state flows through each
step. We implement that pattern explicitly here. Microsoft Agent Framework's
ChatAgent powers the LLM steps; the orchestration is a simple async pipeline so
behavior remains stable across MAF preview versions.
"""
from __future__ import annotations

from pypdf import PdfReader

from app.agents.extractor import build_extractor_agent
from app.agents.validator import build_validator_agent
from app.schemas.invoice import ExtractedInvoice, ValidationReport
from app.workflow.state import AgentState

_extractor = None
_validator = None


def _get_extractor():
    global _extractor
    if _extractor is None:
        _extractor = build_extractor_agent()
    return _extractor


def _get_validator():
    global _validator
    if _validator is None:
        _validator = build_validator_agent()
    return _validator


def _coerce(model_cls, value):
    if isinstance(value, model_cls):
        return value
    if isinstance(value, dict):
        return model_cls.model_validate(value)
    if isinstance(value, str):
        return model_cls.model_validate_json(value)
    # MAF run results may expose .value or .text
    inner = getattr(value, "value", None)
    if inner is not None and not isinstance(inner, type(value)):
        return _coerce(model_cls, inner)
    text = getattr(value, "text", None)
    if isinstance(text, str):
        return model_cls.model_validate_json(text)
    raise TypeError(f"Cannot coerce {type(value)!r} into {model_cls.__name__}")


async def extract_pdf(state: AgentState) -> AgentState:
    """Step 1 — read PDF and produce raw text."""
    reader = PdfReader(state.pdf_path)
    pages = [(p.extract_text() or "") for p in reader.pages]
    state.raw_text = "\n".join(pages).strip()
    return state


async def extract_fields(state: AgentState) -> AgentState:
    """Step 2 — LLM extracts structured fields from raw text."""
    user_msg = f"Invoice raw text:\n---\n{state.raw_text}\n---"
    result = await _get_extractor().run(user_msg)
    state.extracted = _coerce(ExtractedInvoice, result)
    return state


async def validate(state: AgentState) -> AgentState:
    """Step 3 — LLM validates extracted vs expected."""
    assert state.extracted is not None
    payload = (
        f"EXTRACTED:\n{state.extracted.model_dump_json()}\n"
        f"EXPECTED:\n{state.expected.model_dump_json()}"
    )
    result = await _get_validator().run(payload)
    state.validation = _coerce(ValidationReport, result)
    return state


async def run_pipeline(state: AgentState) -> AgentState:
    state = await extract_pdf(state)
    state = await extract_fields(state)
    state = await validate(state)
    return state
