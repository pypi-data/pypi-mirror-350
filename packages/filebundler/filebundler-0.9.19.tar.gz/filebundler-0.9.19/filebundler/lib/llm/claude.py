# filebundler/lib/llm/claude.py
import logfire

from typing import TypeVar, Type

from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.anthropic import AnthropicModelName
from pydantic_ai.providers.anthropic import AnthropicProvider

from filebundler.utils import BaseModel
from filebundler.constants import get_env_settings


# NOTE sadly we need to maintain these manually
ANTHROPIC_MODEL_NAMES = [
    "claude-3-7-sonnet-latest",
    "claude-3-5-sonnet-latest",
    "claude-3-5-haiku-latest",
    "claude-3-opus-latest",
]

T = TypeVar("T", bound=BaseModel)


def anthropic_synchronous_prompt(
    model_type: AnthropicModelName,
    system_prompt: str,
    user_prompt: str,
    result_type: Type[T],
):
    """
    Send a prompt to the LLM and get a structured response.

    Args:
        model_type: The LLM model to use
        system_prompt: The system prompt text
        user_prompt: The user's prompt text
        result_type: The type of the result to return

    Returns:
        Structured response from the LLM
    """
    env_settings = get_env_settings()
    with logfire.span("prompting LLM for auto-bundle", model=model_type, _level="info"):
        model = AnthropicModel(
            # ModelType(model_type).value #  we don't validate here bc the options come from the selectbox
            model_type,
            provider=AnthropicProvider(api_key=env_settings.anthropic_api_key),
        )
        # NOTE on instrument https://ai.pydantic.dev/logfire/#using-logfire
        agent = Agent(
            model, result_type=result_type, system_prompt=system_prompt, instrument=True
        )

        try:
            response = agent.run_sync(user_prompt)
            logfire.info(
                "LLM response received",
                token_usage=response.usage,
            )
            return response.data

        except Exception as e:
            logfire.error(f"Error prompting LLM: {str(e)}", _exc_info=True)
            raise
