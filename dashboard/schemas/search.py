"""Pydantic v2 schemas for Knowledge Base & Entity Search."""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class SearchResultItem(BaseModel):
    id: str
    title: str
    type: str  # kb, issue, decision, session, risk
    snippet: str
    file_path: str
    score: float = 1.0
    tags: List[str] = Field(default_factory=list)


class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[SearchResultItem] = Field(default_factory=list)

