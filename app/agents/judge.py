from agent_framework import Agent, ChatOptions
from pydantic import BaseModel, Field

from app.llm.client import get_judge_client
from app.llm.prompts import JUDGE_INSTRUCTIONS


class JudgeVerdict(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    rationale: str


def build_judge_agent() -> Agent:
    options: ChatOptions = {"response_format": JudgeVerdict}
    return Agent(
        get_judge_client(),
        JUDGE_INSTRUCTIONS,
        default_options=options,
    )
