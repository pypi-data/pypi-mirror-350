from enum import Enum

from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from util_agent.settings import agent_settings


class OpenAIModelName(str, Enum):
    GPT_4O = "gpt-4o"
    O4_MINI = "o4-mini"
    O3_MINI = "o3-mini"


class OpenAIEmbeddingModelName(str, Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"
    TEXT_EMBEDDING_3_LARGE = "text-embedding-3-large"


def get_openai_client():
    return AsyncOpenAI(
        api_key=agent_settings.openai.api_key,
        base_url=agent_settings.openai.base_url,
    )


def get_openai_provider():
    return OpenAIProvider(openai_client=get_openai_client())


def get_openai_model(model_name: OpenAIModelName):
    return OpenAIModel(
        model_name=model_name,
        provider=get_openai_provider(),
    )
