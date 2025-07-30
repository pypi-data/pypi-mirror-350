from typing import Any

from pydantic_ai import Agent

from util_agent.agent_factory import AgentFactory
from util_agent.ark import ArkEmbeddingModelName, ArkModelName, get_ark_client, get_ark_model
from util_agent.azure_openai import (
    AzureOpenAIModelName,
    get_azure_openai_client,
    get_azure_openai_model,
)
from util_agent.openai import OpenAIModelName, get_openai_model
from util_agent.vertex import VertexModelName, get_vertex_model


def create_deepseek_r1_agent(system_prompt: str | None = None) -> Agent[Any, str]:
    return AgentFactory.create_agent(
        model=get_ark_model(ArkModelName.DEEPSEEK_R1),
        system_prompt=system_prompt,
    )


async def create_ark_embedding(
    model_name: ArkEmbeddingModelName, input: str, dimensions: int = 1024
):
    return await AgentFactory.create_embedding(
        client=get_ark_client(),
        model_name=model_name,
        input=input,
        dimensions=dimensions,
    )


def create_openai_gpt_4o_agent(system_prompt: str | None = None) -> Agent[Any, str]:
    return AgentFactory.create_agent(
        model=get_openai_model(OpenAIModelName.GPT_4O),
        system_prompt=system_prompt,
    )


def create_azure_gpt_4o_agent(system_prompt: str | None = None) -> Agent[Any, str]:
    return AgentFactory.create_agent(
        model=get_azure_openai_model(AzureOpenAIModelName.GPT_4O),
        system_prompt=system_prompt,
    )


async def create_azure_openai_embedding(
    model_name: AzureOpenAIModelName,
    input: str,
    dimensions: int = 1024,
):
    return await AgentFactory.create_embedding(
        client=get_azure_openai_client(model_name),
        model_name=model_name,
        input=input,
        dimensions=dimensions,
    )


def create_gpt_4o_agent(system_prompt: str | None = None) -> Agent[Any, str]:
    """
    TODO: for fallback models.
    """
    return AgentFactory.create_agent(
        model=get_openai_model(OpenAIModelName.GPT_4O),
        system_prompt=system_prompt,
    )


def create_o4_mini_agent(system_prompt: str | None = None) -> Agent[Any, str]:
    """
    TODO: for fallback models.
    """
    return AgentFactory.create_agent(
        model=get_azure_openai_model(AzureOpenAIModelName.O4_MINI),
        system_prompt=system_prompt,
    )


def create_gemini_2_5_pro_agent(system_prompt: str | None = None) -> Agent[Any, str]:
    return AgentFactory.create_agent(
        model=get_vertex_model(VertexModelName.GEMINI_2_5_PRO_EXP_03_25),
        system_prompt=system_prompt,
    )
