from enum import Enum

import httpx
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_vertex import GoogleVertexProvider

from util_agent.settings import agent_settings


class VertexModelName(str, Enum):
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite"
    GEMINI_2_0_FLASH_THINKING_EXP_01_21 = "gemini-2.0-flash-thinking-exp-01-21"
    GEMINI_2_5_PRO_EXP_03_25 = "gemini-2.5-pro-exp-03-25"


def get_vertex_provider():
    timeout = 300
    if agent_settings.proxy.enabled:
        http_client = httpx.AsyncClient(
            timeout=timeout,
            proxy=agent_settings.proxy.url,
        )
    else:
        http_client = httpx.AsyncClient(timeout=timeout)

    return GoogleVertexProvider(
        service_account_info=agent_settings.vertex.service_account_info,
        http_client=http_client,
    )


def get_vertex_model(model_name: VertexModelName):
    return GeminiModel(
        model_name=model_name,
        provider=get_vertex_provider(),
    )
