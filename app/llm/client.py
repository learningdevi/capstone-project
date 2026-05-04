from functools import lru_cache

from agent_framework.openai import OpenAIChatClient

from app.config import get_settings


def _build_client(deployment: str) -> OpenAIChatClient:
    s = get_settings()
    # OpenAIChatClient supports Azure OpenAI when azure_endpoint + api_version are set.
    # `model` is the Azure deployment name.
    return OpenAIChatClient(
        model=deployment,
        api_key=s.azure_openai_key,
        azure_endpoint=s.endpoint_base,
        api_version=s.azure_openai_api_version,
    )


@lru_cache
def get_extractor_client() -> OpenAIChatClient:
    return _build_client(get_settings().azure_openai_chat_deployment)


@lru_cache
def get_judge_client() -> OpenAIChatClient:
    return _build_client(get_settings().azure_openai_judge_deployment)
