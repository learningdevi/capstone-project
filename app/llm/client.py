from functools import lru_cache

from agent_framework.openai import OpenAIChatCompletionClient

from app.config import get_settings


def _build_client(deployment: str) -> OpenAIChatCompletionClient:
    s = get_settings()
    # Uses Azure OpenAI's classic /chat/completions endpoint (works with the
    # 2025-01-01-preview API version and earlier).
    return OpenAIChatCompletionClient(
        model=deployment,
        api_key=s.azure_openai_key,
        azure_endpoint=s.endpoint_base,
        api_version=s.azure_openai_api_version,
    )


@lru_cache
def get_extractor_client() -> OpenAIChatCompletionClient:
    return _build_client(get_settings().azure_openai_chat_deployment)


@lru_cache
def get_judge_client() -> OpenAIChatCompletionClient:
    return _build_client(get_settings().azure_openai_judge_deployment)
