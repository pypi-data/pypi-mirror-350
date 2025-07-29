# filebundler/models/llm/AutoBundleResponse.py
from pathlib import Path
from typing import Optional, List

from pydantic import Field

from filebundler.utils import BaseModel


class AutoBundleResponseFiles(BaseModel):
    """Files categorized by relevance. Keys are 'very_likely_useful' and 'probably_useful', values are lists of file paths."""

    very_likely_useful: List[Path] = Field(
        description="Files that are very likely to be useful. In relative paths."
    )
    probably_useful: List[Path] = Field(
        description="Files that are probably useful. In relative paths."
    )


class AutoBundleResponse(BaseModel):
    """Response structure from the LLM for auto-bundling."""

    name: str = Field(description="Name for the auto-generated bundle")
    files: AutoBundleResponseFiles = Field(
        description="Files categorized by relevance. Keys are 'very_likely_useful' and 'probably_useful', values are lists of file paths."
    )
    message: Optional[str] = Field(
        default=None,
        description="Optional message with advice or explanation from the LLM",
    )
    code: Optional[str] = Field(
        default=None,
        description="Optional code",
    )


__all__ = ["AutoBundleResponse"]
