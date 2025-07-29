"""
pdf2podcast - A Python library to convert PDF documents into podcasts.
"""

from .core.base import (
    BasePodcastGenerator,
    BaseRAG,
    BaseLLM,
    BaseTTS,
    BaseChunker,
    BaseRetriever,
    BasePromptBuilder,
)
from .core.rag import (
    AdvancedPDFProcessor as SimplePDFProcessor,
    AdvancedTextProcessor as SimpleTextProcessor,
)  # For backward compatibility
from .core.llm import GeminiLLM
from .core.tts import AWSPollyTTS, GoogleTTS, AzureTTS, KokoroTTS
from .core.prompts import PodcastPromptBuilder
from .core.processing import SimpleChunker, SemanticRetriever

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Main podcast generator class
class PodcastGenerator(BasePodcastGenerator):
    """
    Main class for converting PDFs to podcasts.

    This class provides a simple interface for converting PDF documents
    into audio podcasts using configurable RAG, LLM, and TTS components.
    """

    pass  # Inherits all functionality from BasePodcastGenerator


__version__ = "0.1.0"

__all__ = [
    "PodcastGenerator",
    "SimplePDFProcessor",
    "SimpleTextProcessor",
    "GeminiLLM",
    "AWSPollyTTS",
    "GoogleTTS",
    "AzureTTS",
    "KokoroTTS",
    "BaseRAG",
    "BaseLLM",
    "BaseTTS",
    "BaseChunker",
    "BaseRetriever",
    "SimpleChunker",
    "SemanticRetriever",
]
