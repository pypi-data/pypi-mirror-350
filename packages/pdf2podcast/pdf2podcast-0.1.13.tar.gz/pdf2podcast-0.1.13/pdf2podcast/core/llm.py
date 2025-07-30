"""
Large Language Model (LLM) implementations for pdf2podcast.
"""

import os
import re
import time
import logging
from typing import Dict, Any, Optional, Callable
from functools import wraps
from dotenv import load_dotenv

from langchain.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from google.api_core import retry
from google.api_core.exceptions import GoogleAPIError
from .base import BaseLLM
from .prompts import PodcastPromptBuilder
from .parsers import PodcastParser

# Setup logging
logger = logging.getLogger(__name__)


def retry_on_exception(
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (GoogleAPIError,),
) -> Callable:
    """
    Retry decorator with exponential backoff.

    Args:
        retries (int): Maximum number of retries
        delay (float): Initial delay between retries in seconds
        backoff (float): Backoff multiplier
        exceptions (tuple): Exceptions to catch
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_delay = delay
            last_exception = None

            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if i < retries - 1:
                        logger.warning(
                            f"Attempt {i + 1}/{retries} failed: {str(e)}. "
                            f"Retrying in {retry_delay:.1f}s..."
                        )
                        time.sleep(retry_delay)
                        retry_delay *= backoff
                    else:
                        logger.error(f"All {retries} attempts failed.")

            raise last_exception

        return wrapper

    return decorator


class GeminiLLM(BaseLLM):
    """
    Google's Gemini-based LLM implementation with optimized content generation.
    """

    def __init__(
        self,
        api_key: str = None,
        model_name: str = "gemini-1.5-flash",
        language: str = "en",
        temperature: float = 0.2,
        top_p: float = 0.9,
        max_output_tokens: int = 4096,
        streaming: bool = False,
        prompt_builder: PodcastPromptBuilder = None,
    ):
        """
        Initialize Gemini LLM system.

        Args:
            api_key (str, optional): Google API key. If not provided, will look for GENAI_API_KEY env var
            model_name (str): Name of the Gemini model to use (default: "gemini-1.5-flash")
            temperature (float): Sampling temperature (default: 0.2)
            top_p (float): Nucleus sampling parameter (default: 0.9)
            max_output_tokens (int): Maximum output length (default: 4096)
            streaming (bool): Whether to use streaming mode (default: False)
            prompt_builder (Optional[PodcastPromptBuilder]): Custom prompt builder
        """
        super().__init__(prompt_builder or PodcastPromptBuilder())

        if api_key is None:
            load_dotenv()
            api_key = os.getenv("GENAI_API_KEY")
            if not api_key:
                raise ValueError("No API key provided and GENAI_API_KEY not found")

        self.language = language
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_output_tokens,
            streaming=streaming,
            google_api_key=api_key,
        )

    def _clean_text(self, text: str) -> str:
        """
        Clean text using regex patterns to remove visual references and formatting.

        Args:
            text (str): Input text to clean

        Returns:
            str: Cleaned text with visual references removed
        """
        patterns = [
            r"(Figure|Fig\.|Table|Image)\s+\d+[a-z]?",
            r"(shown|illustrated|depicted|as seen) (in|on|above|below)",
            r"(refer to|see|view) (figure|table|image)",
            r"\(fig\.\s*\d+\)",
            r"as (shown|depicted) (here|below|above)",
        ]

        processed = text
        for pattern in patterns:
            processed = re.sub(pattern, "", processed, flags=re.IGNORECASE)

        processed = re.sub(r"\s+", " ", processed)
        return processed.strip()

    def _expand_content(
        self,
        text: str,
        initial_podcast_model: Any,
        max_attempts: int = 3,
        **kwargs: Dict[str, Any],
    ) -> Any:
        """
        Expand the content of the podcast model to meet minimum length requirements.

        Args:
            text (str): Original text used for context in prompts
            initial_podcast_model (Any): The initial Pydantic model of the podcast (Podcast)
            max_attempts (int): Maximum number of attempts for expansion
            **kwargs: Additional parameters for customization, including:
                - min_length (int): Minimum length of the generated script
                - chapters (bool): Whether the podcast model has chapters

        Returns:
            Any: Expanded Pydantic podcast model
        """
        attempts = 0
        min_length = kwargs.get("min_length", 10000)
        chapters = kwargs.get("chapters", False)

        current_podcast_model = initial_podcast_model

        # Determine current script text and its length
        if chapters:
            script_text_for_length_check = " ".join(
                ch.chapter_content for ch in current_podcast_model.chapters
            )
        else:
            script_text_for_length_check = current_podcast_model.chapter_content

        while (
            len(script_text_for_length_check) < min_length and attempts < max_attempts
        ):
            logger.info(
                f"Attempting to expand script ({len(script_text_for_length_check)} characters) to at least {min_length} characters."
            )
            # Get the expand prompt template, using the current script text
            expand_prompt = self.prompt_builder.build_expand_prompt(
                text=text,  # Original text for context
                script=script_text_for_length_check,  # Current script text for the prompt
                **kwargs,
            )

            # Create the parser for the expansion chain
            # The parser type for expansion should match the initial model type
            logger.info("Creating podcast chain for expansion...")
            expansion_parser = PodcastParser()

            # Get the main prompt object to extract its style
            main_prompt_style_template = self.prompt_builder.build_prompt(
                text=text,
                **kwargs,
            )

            # Format this main prompt template with its necessary inputs,
            # providing empty format_instructions as we only want its stylistic content.
            stylistic_guidance_text = main_prompt_style_template.format(
                text=text,
                query=kwargs.get("query", ""),
                instructions=kwargs.get(
                    "instructions", ""
                ),  # These are the original instructions
                format_instructions="",  # Resolve main prompt's format instructions to empty
                language=self.language,  # Add language for stylistic guidance
            )

            # Get format instructions specifically for the expansion output
            format_instructions_for_expand = expansion_parser.get_format_instructions()

            # General instructions for the EXPAND_PROMPT itself (distinct from those used for stylistic_guidance_text)
            expand_prompt_general_instructions = kwargs.get("instructions", "")

            input_for_expand_prompt_template = {
                "current_length": len(script_text_for_length_check),
                "min_length": min_length,
                "query": kwargs.get("query", ""),
                "instructions": expand_prompt_general_instructions,  # General instructions for EXPAND_PROMPT
                "format_instructions": format_instructions_for_expand,  # Specific format instructions for EXPAND_PROMPT output
                "script": script_text_for_length_check,
                "system_prompt": stylistic_guidance_text,  # Use the pre-formatted stylistic guide
                "language": self.language,  # Add language for expansion
            }

            chain = expand_prompt | self.llm | expansion_parser
            current_podcast_model = chain.invoke(
                input_for_expand_prompt_template
            )  # This is the new Pydantic model

            # Update script_text_for_length_check for the next iteration
            if chapters:
                script_text_for_length_check = " ".join(
                    ch.chapter_content for ch in current_podcast_model.chapters
                )
            else:
                script_text_for_length_check = current_podcast_model.chapter_content

            script_text_for_length_check = script_text_for_length_check.strip()
            attempts += 1

        if len(script_text_for_length_check) < min_length:
            logger.info(f"Failed to expand script to required length ({min_length})")

        return current_podcast_model  # Return the Pydantic model

    @retry_on_exception()
    def generate_podcast_script(
        self,
        text,
        **kwargs: Dict[str, Any],
    ) -> str:
        """
        Generate a coherent podcast script.

        Args:
            **kwargs: Additional parameters for customization, including:
                - text (str): Input text to convert into a podcast script
                - min_length (int): Minimum length of the generated script
                - max_attempts (int): Maximum attempts for expansion
                - chapters (bool): Whether to use chapters in the output
                - query (str): Optional query to guide content generation
                - instructions (str): Optional additional instructions for generation

        Returns:
            str: Generated podcast script
        """
        try:
            # Clean and validate input text
            if not text or not text.strip():
                raise ValueError("Input text cannot be empty")

            processed_text = self._clean_text(text)
            if not processed_text:
                raise ValueError("Text cleaning resulted in empty content")

            min_length = kwargs.get("min_length", 10000)
            chapters = kwargs.get("chapters", False)

            # Generate initial script
            try:
                # Get the prompt template with language
                prompt_template = self.prompt_builder.build_prompt(
                    text=processed_text,
                    **kwargs,
                )

                # Create the chain based on format
                logger.info("Creating podcast chain...")
                parser = PodcastParser()

                # Create chain with properly formatted prompt and format variables
                chain = prompt_template | self.llm | parser

                # Get format instructions from the selected parser
                format_instructions = parser.get_format_instructions()

                input_variables = {
                    "text": processed_text,
                    "query": kwargs.get("query", ""),
                    "instructions": kwargs.get("instructions", ""),
                    "format_instructions": format_instructions,
                    "language": self.language,
                }

                result = chain.invoke(input_variables)

                # Get text content for length check
                text_content = " ".join(ch.chapter_content for ch in result.chapters)

                # Expand if needed
                if len(text_content) < min_length:
                    logger.info(
                        f"Initial script length ({len(text_content)}) below target ({min_length}). "
                        "Expanding content..."
                    )
                    result = self._expand_content(
                        text=processed_text,
                        initial_podcast_model=result,  # Pass the Pydantic model
                        **kwargs,
                    )
                    # No need to parse again, _expand_content now returns a Pydantic model

                logger.info(f"Successfully generated script")
                return result.model_dump_json()

            except GoogleAPIError as e:
                logger.error(f"Google API error: {str(e)}")
                raise  # Will be caught by retry decorator
            except Exception as e:
                logger.error(f"Unexpected error in script generation: {str(e)}")
                raise Exception(f"Failed to generate podcast script: {str(e)}")

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Script generation failed: {str(e)}")
            raise
