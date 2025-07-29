"""
Base abstract classes for the pdf2podcast library components.
"""

import json  # Added import
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BasePromptBuilder(ABC):
    """Base class for building prompts."""

    @abstractmethod
    def build_prompt(self, text: str, **kwargs) -> "PromptTemplate":
        """
        Build a prompt for content generation.

        Args:
            text (str): Source text
            **kwargs: Additional prompt parameters

        Returns:
            PromptTemplate: Formatted prompt template
        """
        pass

    @abstractmethod
    def build_expand_prompt(self, text: str, **kwargs) -> "PromptTemplate":
        """
        Build a prompt for content expansion.

        Args:
            text (str): Current content
            **kwargs: Additional prompt parameters

        Returns:
            PromptTemplate: Formatted expansion prompt template
        """
        pass


class BaseRAG(ABC):
    """Base class for RAG (Retrieval Augmented Generation) implementations."""

    @abstractmethod
    def process(self, pdf_path: str) -> str:
        """
        Process a PDF document and extract relevant text content.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            str: Extracted and processed text from the PDF
        """
        pass


class BaseChunker(ABC):
    """Base class for text chunking implementations."""

    @abstractmethod
    def chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """
        Split text into manageable chunks.

        Args:
            text (str): Text to be chunked
            chunk_size (int): Maximum size of each chunk in characters

        Returns:
            List[str]: List of text chunks
        """
        pass


class BaseRetriever(ABC):
    """Base class for semantic text retrieval implementations."""

    @abstractmethod
    def add_texts(self, texts: List[str]) -> None:
        """
        Add texts to the retrieval system.

        Args:
            texts (List[str]): List of text chunks to be indexed
        """
        pass

    @abstractmethod
    def get_relevant_chunks(self, query: str, k: int = 3) -> List[str]:
        """
        Retrieve most relevant text chunks for a query.

        Args:
            query (str): Query text to find relevant chunks for
            k (int): Number of chunks to retrieve (default: 3)

        Returns:
            List[str]: List of relevant text chunks
        """
        pass


class BaseLLM(ABC):
    """Base class for Large Language Model implementations."""

    def __init__(self, prompt_builder: Optional[BasePromptBuilder] = None):
        """
        Initialize LLM with optional prompt builder.

        Args:
            prompt_builder (Optional[BasePromptBuilder]): Custom prompt builder
        """
        self.prompt_builder = prompt_builder

    @abstractmethod
    def generate_podcast_script(self, text: str, **kwargs: Dict[str, Any]) -> str:
        """
        Generate a podcast script from input text.

        Args:
            text (str): Input text to convert into a podcast script
            **kwargs: Additional model-specific parameters including:

        Returns:
            str: Generated podcast script (as a JSON string)
        """
        pass


class BaseTTS(ABC):
    """Base class for Text-to-Speech implementations."""

    @abstractmethod
    def generate_audio(
        self,
        text_segments: List[str],  # Changed from text: str to text_segments: List[str]
        output_path: str,
        voice_id: Optional[str] = None,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Convert text segments to speech and save as audio file.
        If multiple segments, they will be concatenated.

        Args:
            text_segments (List[str]): List of text segments to convert to speech
            output_path (str): Path where to save the audio file
            voice_id (Optional[str]): ID of the voice to use
            **kwargs: Additional TTS-specific parameters

        Returns:
            Dict[str, Any]: Dictionary containing audio metadata
                          (e.g., {'duration': float, 'size': int})
        """
        pass


class BasePodcastGenerator:
    """Base class for podcast generation orchestration."""

    def __init__(
        self,
        rag_system: BaseRAG,
        llm_provider: str,
        tts_provider: str,
        llm_config: Optional[Dict[str, Any]] = None,
        tts_config: Optional[Dict[str, Any]] = None,
        chunker: Optional[BaseChunker] = None,
        retriever: Optional[BaseRetriever] = None,
        k: int = 3,
    ):
        """
        Initialize podcast generator with required components.

        Args:
            rag_system (BaseRAG): System for PDF text extraction
            llm_provider (str): Type of LLM to use ("gemini", "openai", etc.)
            tts_provider (str): Type of TTS to use ("aws", "google", etc.)
            llm_config (Optional[Dict[str, Any]]): Configuration for LLM
            tts_config (Optional[Dict[str, Any]]): Configuration for TTS
            chunker (Optional[BaseChunker]): System for text chunking
            retriever (Optional[BaseRetriever]): System for semantic retrieval
            k (int): Number of chunks to retrieve for a query (default: 3)
        """
        from .managers import LLMManager, TTSManager

        self.rag = rag_system

        # Initialize models using managers
        llm_manager = LLMManager(llm_provider, **(llm_config or {}))
        tts_manager = TTSManager(tts_provider, **(tts_config or {}))

        self.llm = llm_manager.get_llm()
        self.tts = tts_manager.get_tts()
        self.chunker = chunker
        self.retriever = retriever
        self.k = k

    def generate(
        self,
        pdf_path: Optional[str] = None,
        voice_id: Optional[str] = None,
        output_path: str = "output.mp3",
        text: str = None,
        **kwargs: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a podcast from a PDF document.

        Args:
            pdf_path (str): Path to the input PDF file
            output_path (str): Path where to save the output audio file
            voice_id (Optional[str]): ID of the voice to use for TTS
            text (str): Optional text input for podcast generation
            **kwargs: Additional parameters for RAG, LLM, or TTS systems

        Returns:
            Dict[str, Any]: Dictionary containing generation results and metadata
        """
        # Extract text from PDF
        if pdf_path:
            processed_text_for_llm = self.rag.process(pdf_path)
        elif text:
            # If text is directly provided, assume it's already processed or doesn't need RAG
            processed_text_for_llm = text
        else:
            raise ValueError("Either pdf_path or text must be provided.")

        # Process with chunking and retrieval if available and if pdf_path was used
        if self.chunker and self.retriever:
            chunks = self.chunker.chunk_text(processed_text_for_llm)
            self.retriever.add_texts(chunks)

            query = kwargs.get("query")
            if not query:
                # Use default query if none provided
                query = "Generate a podcast script based on the extracted text."

            # Use retrieved chunks to generate the script
            relevant_chunks = self.retriever.get_relevant_chunks(query, k=self.k)
            processed_text_for_llm = "\n\n".join(relevant_chunks)

        # Generate podcast script (which is a JSON string)
        script_json_string = self.llm.generate_podcast_script(
            text=processed_text_for_llm,
            **kwargs,
        )

        # Parse the JSON string into a Python dictionary
        parsed_script_data = json.loads(script_json_string)

        script_segments_for_tts: List[str]
        use_chapters_flag = kwargs.get("chapters", False)

        if use_chapters_flag:
            # If chapters are requested, extract text from each chapter
            # Assumes parsed_script_data has a "chapters" key with a list of chapter dicts
            if "chapters" in parsed_script_data and isinstance(
                parsed_script_data["chapters"], list
            ):
                script_segments_for_tts = [
                    chapter.get("chapter_content", "")
                    for chapter in parsed_script_data["chapters"]
                ]
            else:
                # Fallback or error if structure is not as expected
                script_segments_for_tts = [
                    parsed_script_data.get("chapter_content", "")
                ]  # Or raise error
                print(
                    "Warning: 'chapters' was True, but 'chapters' key not found or not a list in parsed script. Using main text."
                )
        else:
            # If chapters are not requested, use the entire script text
            # Assumes parsed_script_data has a "text" key
            script_segments_for_tts = [parsed_script_data.get("text", "")]

        # Process chapters individually to get timing data
        audio_result = self.tts.generate_audio(
            text_segments=script_segments_for_tts,
            output_path=output_path,
            voice_id=voice_id,
            **kwargs,
        )

        if audio_result.get("timing_data") and "chapters" in parsed_script_data:
            # Update chapter timing information in the script
            for chapter, timing in zip(
                parsed_script_data["chapters"], audio_result["timing_data"]["chapters"]
            ):
                chapter["start_time"] = timing["start_time"]
                chapter["end_time"] = timing["end_time"]
                chapter["duration"] = timing["duration"]
                chapter["word_timings"] = timing["word_timings"]

        return {
            "script": parsed_script_data,
            "audio": audio_result,
            "total_duration": audio_result.get("timing_data", {}).get(
                "total_duration", 0.0
            ),
        }
