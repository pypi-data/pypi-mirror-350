import logfire
import os

from typing import TypeVar, Type

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel, GeminiModelName
from pydantic_ai.providers.google_gla import GoogleGLAProvider

from filebundler.utils import BaseModel
from filebundler.constants import get_env_settings

# NOTE: Maintain this list manually, similar to ANTHROPIC_MODEL_NAMES
GEMINI_MODEL_NAMES = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-1.0-pro",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking-exp-01-21",
    "gemini-exp-1206",
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-2.0-pro-exp-02-05",
    "gemini-2.5-flash-preview-04-17",
    "gemini-2.5-pro-exp-03-25",
    "gemini-2.5-pro-preview-03-25",
]

T = TypeVar("T", bound=BaseModel)


def gemini_synchronous_prompt(
    model_type: GeminiModelName,
    system_prompt: str,
    user_prompt: str,
    result_type: Type[T],
):
    """
    Send a prompt to the Gemini LLM and get a structured response.

    Args:
        model_type: The Gemini model to use
        system_prompt: The system prompt text
        user_prompt: The user's prompt text
        result_type: The type of the result to return

    Returns:
        Structured response from the LLM
    """
    env_settings = get_env_settings()
    api_key = getattr(env_settings, "gemini_api_key", None) or os.environ.get(
        "GEMINI_API_KEY"
    )
    if not api_key:
        logfire.error("No Gemini API key found in environment or settings.")
        raise ValueError("Gemini API key is required.")
    with logfire.span(
        "prompting Gemini LLM for auto-bundle", model=model_type, _level="info"
    ):
        model = GeminiModel(
            model_type,
            provider=GoogleGLAProvider(api_key=api_key),
        )
        agent = Agent(
            model, result_type=result_type, system_prompt=system_prompt, instrument=True
        )
        try:
            response = agent.run_sync(user_prompt)
            logfire.info(
                "Gemini LLM response received",
                token_usage=response.usage,
            )
            return response.data
        except Exception as e:
            logfire.error(f"Error prompting Gemini LLM: {str(e)}", _exc_info=True)
            raise
