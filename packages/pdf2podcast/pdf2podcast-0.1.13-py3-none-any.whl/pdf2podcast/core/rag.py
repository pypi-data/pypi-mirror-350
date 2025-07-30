"""
Retrieval Augmented Generation (RAG) implementations for pdf2podcast.
"""

from typing import List, Optional, Dict
from pypdf import PdfReader
from .base import BaseRAG


class AdvancedPDFProcessor(BaseRAG):
    """
    Advanced PDF text extraction implementation.

    This class provides enhanced PDF text extraction functionality using PyPDF2.
    It processes PDF documents and returns their text content in a format
    suitable for podcast script generation.
    """

    def __init__(
        self,
        max_chars_per_chunk: int = 4000,
        extract_images: bool = False,
        metadata: bool = True,
        chunker=None,
        retriever=None,
    ):
        """
        Initialize PDF processor.

        Args:
            max_chars_per_chunk (int): Maximum characters per text chunk (default: 4000)
            extract_images (bool): Whether to extract image captions (default: False)
            metadata (bool): Whether to include document metadata (default: True)
            chunker (Optional[BaseChunker]): Custom text chunker (default: SimpleChunker)
            retriever (Optional[BaseRetriever]): Custom text retriever
        """
        from .processing import SimpleChunker

        self.max_chars_per_chunk = max_chars_per_chunk
        self.include_metadata = metadata
        self.chunker = chunker or SimpleChunker()
        self.retriever = retriever

    def process(self, pdf_path: str) -> str:
        """
        Process a PDF document and extract its text content.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            str: Extracted and processed text from the PDF

        Raises:
            Exception: If PDF processing fails
        """
        try:
            # Open the PDF using PyPDF2
            with open(pdf_path, "rb") as file:
                reader = PdfReader(file)
                content_parts = []

                # Extract metadata if enabled
                if self.include_metadata:
                    metadata = self._extract_metadata(reader)
                    if metadata:
                        content_parts.append(metadata)

                # Process each page
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        # Clean up text
                        text = self._clean_text(text)
                        content_parts.append(text)

            # Join all content
            full_text = "\n\n".join(content_parts)

            # Instead of truncating, use chunker to split text
            chunks = self.chunker.chunk_text(full_text, self.max_chars_per_chunk)

            # If retriever is available, add chunks to it
            if self.retriever:
                self.retriever.add_texts(chunks)

            # Join chunks back together (they'll be retrieved later if needed)
            return "\n\n".join(chunks)

        except Exception as e:
            raise Exception(f"Failed to process PDF: {str(e)}")

    def _extract_metadata(self, reader: PdfReader) -> Optional[str]:
        """
        Extract relevant metadata from the PDF document.

        Args:
            reader (PdfReader): The PDF reader object

        Returns:
            Optional[str]: Formatted metadata string or None if no metadata found
        """
        metadata = reader.metadata
        if not metadata:
            return None

        meta_parts = []
        # Map PyPDF2 metadata fields to human-readable names
        field_mapping = {
            "/Title": "Title",
            "/Author": "Author",
            "/Subject": "Subject",
            "/Keywords": "Keywords",
            "/Producer": "Producer",
            "/Creator": "Creator",
        }

        for key, display_name in field_mapping.items():
            value = metadata.get(key)
            if value:
                # Clean up the value - remove PDF notation if present
                if isinstance(value, str):
                    value = value.strip("()/")
                meta_parts.append(f"{display_name}: {value}")

        if meta_parts:
            return "Document Information:\n" + "\n".join(meta_parts)

        return None

    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by removing unnecessary whitespace and artifacts.

        Args:
            text (str): Raw text to clean

        Returns:
            str: Cleaned text
        """
        # Remove multiple spaces
        text = " ".join(text.split())

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Remove multiple newlines
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")

        # Remove common PDF artifacts
        text = text.replace("•", "")  # Remove bullet points
        text = text.strip()

        return text

    def _truncate_to_complete_sentence(self, text: str, max_length: int) -> str:
        """
        Truncate text to specified length while keeping complete sentences.

        Args:
            text (str): Text to truncate
            max_length (int): Maximum length of the truncated text

        Returns:
            str: Truncated text ending with a complete sentence
        """
        if len(text) <= max_length:
            return text

        # Find the last sentence boundary before max_length
        truncated = text[:max_length]

        # Look for common sentence endings
        for end in [".", "!", "?"]:
            last_period = truncated.rfind(end)
            if last_period != -1:
                return text[: last_period + 1]

        # If no sentence boundary found, look for the last complete word
        last_space = truncated.rfind(" ")
        if last_space != -1:
            return text[:last_space]

        return truncated


class AdvancedTextProcessor(BaseRAG):
    """
    Advanced text processing implementation for content generation.

    This class provides advanced text processing capabilities, including
    content generation and expansion using a language model.
    """

    def __init__(self, max_chars_per_chunk: int, chunker=None, retriever=None):
        """
        Initialize text processor.

        Args:
            max_chars_per_chunk (int): Maximum characters per chunk
            chunker (Optional[BaseChunker]): Custom text chunker
            retriever (Optional[BaseRetriever]): Custom text retriever
        """
        from .processing import SimpleChunker

        self.max_chars_per_chunk = max_chars_per_chunk
        self.chunker = chunker or SimpleChunker()
        self.retriever = retriever

    def process(self, text: str) -> str:
        """
        Process a text and extract its content.

        Args:
            text (str): text to process

        Returns:
            str: Extracted and processed text

        Raises:
            Exception: If processing fails
        """
        try:
            # Instead of truncating, use chunker to split text
            chunks = self.chunker.chunk_text(text, self.max_chars_per_chunk)

            # If retriever is available, add chunks to it
            if self.retriever:
                self.retriever.add_texts(chunks)

            # Join chunks back together (they'll be retrieved later if needed)
            return "\n\n".join(chunks)

        except Exception as e:
            raise Exception(f"Failed to process text: {str(e)}")
