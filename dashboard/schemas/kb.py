"""Pydantic v2 schemas for Knowledge Base articles and link graphs."""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict


class KBArticleSchema(BaseModel):
    """Schema for Knowledge Base article in .along/KB/ or docs/."""
    model_config = ConfigDict(extra="ignore")

    id: str = Field(..., description="Unique article ID, e.g. kb--architecture or docs--setup")
    slug: str = Field(..., description="Article slug or filename")
    title: str = Field(..., description="Article title")
    type: Literal["topic", "architecture", "domain-model", "setup-workflow", "index", "doc"] = Field(
        default="topic", description="Article topic category"
    )
    created: Optional[str] = Field(None, description="Creation date YYYY-MM-DD")
    updated: Optional[str] = Field(None, description="Last update date YYYY-MM-DD")
    tags: List[str] = Field(default_factory=list, description="List of topic tags")
    file_path: str = Field(..., description="Relative path in repository")
    body: str = Field(default="", description="Markdown body")
    headings: List[str] = Field(default_factory=list, description="Extracted Markdown headings")
    outgoing_links: List[str] = Field(default_factory=list, description="Outgoing wiki or entity links")
    incoming_links: List[str] = Field(default_factory=list, description="Incoming links referencing this article")


class KBGraphNode(BaseModel):
    id: str
    label: str
    type: str
    category: str
    tags: List[str] = Field(default_factory=list)


class KBGraphEdge(BaseModel):
    source: str
    target: str
    type: str
    label: Optional[str] = None


class KBGraphSchema(BaseModel):
    """Bidirectional graph of Knowledge Base articles and related entities."""
    nodes: List[KBGraphNode] = Field(default_factory=list)
    edges: List[KBGraphEdge] = Field(default_factory=list)

