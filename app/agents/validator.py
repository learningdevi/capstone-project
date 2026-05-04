from agent_framework import Agent, ChatOptions

from app.llm.client import get_extractor_client
from app.llm.prompts import VALIDATOR_INSTRUCTIONS
from app.schemas.invoice import ValidationReport


def build_validator_agent() -> Agent:
    options: ChatOptions = {"response_format": ValidationReport}
    return Agent(
        get_extractor_client(),
        VALIDATOR_INSTRUCTIONS,
        default_options=options,
    )
