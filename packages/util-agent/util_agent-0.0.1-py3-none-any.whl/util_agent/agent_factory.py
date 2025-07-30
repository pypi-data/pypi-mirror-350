from typing import Any, Type

from openai import AsyncAzureOpenAI, AsyncOpenAI
from openai.types.create_embedding_response import CreateEmbeddingResponse
from pydantic_ai import Agent, EndStrategy
from pydantic_ai.models.openai import Model


class AgentFactory:
    """Factory class for creating different types of agents."""

    DEFAULT_SYSTEM_PROMPT = 'system'
    DEFAULT_RETRIES = 3
    DEFAULT_DEPS_TYPE = str
    DEFAULT_END_STRATEGY: EndStrategy = 'early'

    @staticmethod
    def create_agent(
        model: Model,
        system_prompt: str | None = None,
        deps_type: Type[Any] | None = None,
        retries: int | None = None,
    ) -> Agent[Any, str]:
        """
        Create an agent with the specified configuration.

        Args:
            client: The OpenAI client to use
            model_name: Name of the model to use
            system_prompt: System prompt for the agent
            deps_type: Type for dependencies
            retries: Number of retries for failed requests

        Returns:
            Configured Agent instance
        """
        return Agent(
            model,
            retries=retries or AgentFactory.DEFAULT_RETRIES,
            deps_type=deps_type or AgentFactory.DEFAULT_DEPS_TYPE,
            system_prompt=system_prompt or AgentFactory.DEFAULT_SYSTEM_PROMPT,
            end_strategy=AgentFactory.DEFAULT_END_STRATEGY,
        )

    @staticmethod
    async def create_embedding(
        client: AsyncOpenAI | AsyncAzureOpenAI,
        model_name: str,
        input: str,
        dimensions: int = 1024,
    ) -> CreateEmbeddingResponse:
        return await client.embeddings.create(
            model=model_name,
            input=input,
            dimensions=dimensions,
        )
