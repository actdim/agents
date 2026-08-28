"""Knowledge Base REST API endpoints."""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from ..schemas.kb import KBArticleSchema, KBGraphSchema
from ..schemas.search import SearchResponse
from ..core.collector import EntityCollector
from ..core.kb_engine import KBEngine

router = APIRouter(prefix="/kb", tags=["Knowledge Base"])


def get_collector() -> EntityCollector:
    raise NotImplementedError


def get_kb_engine(collector: EntityCollector = Depends(get_collector)) -> KBEngine:
    collector.collect_all()
    return KBEngine(collector)


@router.get("", response_model=List[KBArticleSchema], summary="List all Knowledge Base articles")
def list_articles(
    type: Optional[str] = Query(None, description="Filter by category type"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    collector: EntityCollector = Depends(get_collector),
):
    collector.collect_all()
    articles = collector.kb_articles
    if type:
        articles = [a for a in articles if a.type == type]
    if tag:
        articles = [a for a in articles if tag.lower() in [t.lower() for t in a.tags]]
    return articles


@router.get("/search", response_model=SearchResponse, summary="Search Knowledge Base and entities")
def search_kb(
    q: str = Query("", description="Search query string"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    type: Optional[str] = Query(None, description="Filter by entity type (kb, issue, decision, session)"),
    engine: KBEngine = Depends(get_kb_engine),
):
    return engine.search(query=q, tag=tag, entity_type=type)


@router.get("/graph", response_model=KBGraphSchema, summary="Get Knowledge Base cross-link graph")
def get_kb_graph(engine: KBEngine = Depends(get_kb_engine)):
    return engine.build_kb_graph()


@router.get("/{slug}", response_model=KBArticleSchema, summary="Get single Knowledge Base article")
def get_article(slug: str, collector: EntityCollector = Depends(get_collector)):
    collector.collect_all()
    for art in collector.kb_articles:
        if art.slug == slug or art.id == slug:
            return art
    raise HTTPException(status_code=404, detail=f"Article '{slug}' not found in Knowledge Base")

