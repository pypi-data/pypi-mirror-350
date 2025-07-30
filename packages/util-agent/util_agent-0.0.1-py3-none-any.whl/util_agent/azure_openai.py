from enum import Enum

from openai import AsyncAzureOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from util_agent.settings import agent_settings


class AzureOpenAIModelName(str, Enum):
    GPT_4O = "gpt-4o"
    O3_MINI = "o3-mini"
    O4_MINI = "o4-mini"


class AzureOpenAIEmbeddingModelName(str, Enum):
    TEXT_EMBEDDING_3_SMALL = "text-embedding-3-small"


def get_azure_openai_client(model_name: AzureOpenAIModelName):
    deployment = agent_settings.azure_openai.__getattribute__(
        f"{model_name.value}_endpoint".replace("-", "_")
    )
    if deployment is None:
        raise ValueError(f"Invalid model name: {model_name}")
    return AsyncAzureOpenAI(
        api_version=agent_settings.azure_openai.api_version,
        azure_endpoint=agent_settings.azure_openai.base_url,
        api_key=agent_settings.azure_openai.api_key,
        azure_deployment=deployment,
    )


def get_azure_openai_provider(model_name: AzureOpenAIModelName):
    return OpenAIProvider(openai_client=get_azure_openai_client(model_name))


def get_azure_openai_model(model_name: AzureOpenAIModelName):
    return OpenAIModel(
        model_name=model_name,
        provider=get_azure_openai_provider(model_name),
    )
