from agent_framework import Agent, ChatOptions

from app.llm.client import get_extractor_client
from app.llm.prompts import EXTRACTOR_INSTRUCTIONS
from app.schemas.invoice import ExtractedInvoice


def build_extractor_agent() -> Agent:
    options: ChatOptions = {"response_format": ExtractedInvoice}
    return Agent(
        get_extractor_client(),
        EXTRACTOR_INSTRUCTIONS,
        default_options=options,
    )
