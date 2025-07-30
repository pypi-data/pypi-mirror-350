from filebundler.lib.llm.claude import (
    ANTHROPIC_MODEL_NAMES,
    anthropic_synchronous_prompt,
)
from filebundler.lib.llm.gemini import GEMINI_MODEL_NAMES, gemini_synchronous_prompt

# Map each model name to its corresponding prompt function
MODEL_REGISTRY = {
    **{m: anthropic_synchronous_prompt for m in ANTHROPIC_MODEL_NAMES},
    **{m: gemini_synchronous_prompt for m in GEMINI_MODEL_NAMES},
}

# Map each model name to its provider label
PROVIDER_FOR_MODEL = {
    **{m: "Anthropic" for m in ANTHROPIC_MODEL_NAMES},
    **{m: "Gemini" for m in GEMINI_MODEL_NAMES},
}
