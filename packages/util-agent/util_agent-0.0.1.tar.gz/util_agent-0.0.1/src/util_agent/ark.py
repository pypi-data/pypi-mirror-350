from enum import Enum

from openai import AsyncOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from util_agent.settings import agent_settings


class ArkModelName(str, Enum):
    DEEPSEEK_R1 = "deepseek-r1"
    DOUBAO_1_5_VISION_PRO = "doubao-1.5-vision-pro"
    DOUBAO_1_5_THINKING_PRO = "doubao-1.5-thinking-pro"


class ArkEmbeddingModelName(str, Enum):
    EMBEDDING_VISION = "doubao-embedding-vision"
    EMBEDDING_LARGE_TEXT_240915 = "doubao-embedding-large-text-240915"
    EMBEDDING_TEXT_240715 = "doubao-embedding-text-240715"


def get_ark_client():
    return AsyncOpenAI(
        api_key=agent_settings.ark.api_key,
        base_url=agent_settings.ark.base_url,
    )


def get_ark_provider():
    return OpenAIProvider(openai_client=get_ark_client())


def get_ark_model(model_name: ArkModelName):
    _model_name = agent_settings.ark.__getattribute__(
        f"{model_name.value}_endpoint".replace("-", "_")
    )
    if _model_name is None:
        raise ValueError(f"Invalid model name: {model_name}")
    return OpenAIModel(
        model_name=_model_name,
        provider=get_ark_provider(),
    )
