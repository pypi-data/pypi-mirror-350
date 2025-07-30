"""
Prompt templates and mappings for podcast generation using LangChain.
"""

from typing import Dict, Any, Optional
from langchain_core.prompts import PromptTemplate

from pdf2podcast.core.base import BasePromptBuilder
from pdf2podcast.core.prompt_list import (
    DEFAULT_SYSTEM_PROMPT,
    CHAPTERED_SYSTEM_PROMPT,
    EXPAND_PROMPT,
)

# Template per podcast standard senza capitoli
DEFAULT_TEMPLATE = PromptTemplate(
    template=DEFAULT_SYSTEM_PROMPT,
    input_variables=[
        "text",
        "query",
        "instructions",
        "format_instructions",
        "language",
    ],
)

# Template per podcast con capitoli
CHAPTERED_TEMPLATE = PromptTemplate(
    template=CHAPTERED_SYSTEM_PROMPT,
    input_variables=[
        "text",
        "query",
        "instructions",
        "format_instructions",
        "language",
    ],
)

# Template per l'espansione del testo
EXPAND_TEMPLATE = PromptTemplate(
    template=EXPAND_PROMPT,
    input_variables=[
        "current_length",
        "min_length",
        "system_prompt",
        "query",
        "instructions",
        "script",
        "format_instructions",  # Added format_instructions here
        "language",
    ],
)


class PodcastPromptTemplate:
    """Template provider for podcast generation prompts using LangChain."""

    def __init__(
        self,
        system_prompt: Optional[str] = None,
        instructions: Optional[str] = None,
        chapters: bool = False,
    ):
        """
        Initialize template provider with optional custom system prompt.

        Args:
            system_prompt (Optional[str]): Custom system prompt to override default
            instructions (Optional[str]): Additional instructions to include
            chapters (bool): Whether to use chaptered template
        """
        # Scegliamo il template base in base al parametro chapters e al system prompt custom
        if system_prompt:
            # Se viene fornito un prompt personalizzato, creiamo un nuovo template
            self.template = PromptTemplate(
                template=system_prompt,
                input_variables=[
                    "text",
                    "query",
                    "instructions",
                    "format_instructions",
                    "language",
                ],
            )
        else:
            # Altrimenti usiamo uno dei template predefiniti
            self.template = CHAPTERED_TEMPLATE if chapters else DEFAULT_TEMPLATE

        self.instructions = instructions or ""
        self.expand_template = EXPAND_TEMPLATE


class PodcastPromptBuilder(BasePromptBuilder):
    """Prompt builder for podcast script generation."""

    def __init__(
        self,
        template_provider=None,
        system_prompt: Optional[str] = None,
        instructions: Optional[str] = None,
        chapters: bool = False,
    ):
        """
        Initialize with optional custom template provider and system prompt.

        Args:
            template_provider: Template provider class (default: PodcastPromptTemplate)
            system_prompt: Optional custom system prompt to override default
            instructions: Additional instructions to include
            chapters (bool): Whether to use chaptered template
        """
        if template_provider is None:
            template_provider = PodcastPromptTemplate
        self.templates = template_provider(
            system_prompt=system_prompt,
            instructions=instructions,
            chapters=chapters,
        )

    def build_prompt(self, text: str, **kwargs) -> PromptTemplate:
        """Build main generation prompt."""
        return self.templates.template

    def build_expand_prompt(self, text: str, **kwargs) -> PromptTemplate:
        """Build expansion prompt."""
        return self.templates.expand_template
