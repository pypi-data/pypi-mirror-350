"""
Parsers for handling LLM outputs in specific formats.
"""

from typing import List
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class PodcastChapter(BaseModel):
    """Model for a single podcast chapter."""

    position: int = Field(description="Position of the chapter in the sequence")
    title: str = Field(description="Title of the chapter")
    chapter_content: str = Field(description="Content of the chapter")


class Podcast(BaseModel):
    """Model for a complete podcast with chapters and metadata."""

    chapters: List[PodcastChapter] = Field(
        description="List of chapters in the podcast"
    )
    title: str = Field(description="Title of the podcast")
    tags: List[str] = Field(description="List of tags for the podcast")


class PodcastParser(PydanticOutputParser):
    """Parser for podcast content with chapters and metadata."""

    def __init__(self) -> None:
        super().__init__(pydantic_object=Podcast)

    def parse(self, text: str) -> Podcast:
        """Parse the text into a Podcast object with chapters and metadata."""
        return super().parse(text)
