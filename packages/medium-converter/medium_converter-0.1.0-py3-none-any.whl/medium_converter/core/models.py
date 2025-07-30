"""Data models for Medium Converter."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ContentType(str, Enum):
    """Types of content blocks in Medium articles."""

    TEXT = "text"
    IMAGE = "image"
    CODE = "code"
    QUOTE = "quote"
    LIST = "list"
    HEADING = "heading"


class ContentBlock(BaseModel):
    """A block of content in a Medium article."""

    type: ContentType
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class Section(BaseModel):
    """A section of a Medium article."""

    title: str | None = None
    blocks: list[ContentBlock] = Field(default_factory=list)


class Article(BaseModel):
    """A Medium article."""

    title: str
    author: str
    date: str | datetime
    content: list[Section | ContentBlock] = Field(default_factory=list)
    estimated_reading_time: int | None = None
    url: str | None = None
    tags: list[str] = Field(default_factory=list)
