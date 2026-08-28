"""Knowledge Base Search and Cross-Link Engine."""

import re
from typing import List, Dict, Optional, Any
from ..schemas.kb import KBArticleSchema, KBGraphSchema, KBGraphNode, KBGraphEdge
from ..schemas.search import SearchResultItem, SearchResponse
from .collector import EntityCollector


class KBEngine:
    """In-memory indexing, full-text search, and link-graph resolution for Knowledge Base."""

    def __init__(self, collector: EntityCollector):
        self.collector = collector

    def search(self, query: str, tag: Optional[str] = None, entity_type: Optional[str] = None) -> SearchResponse:
        """Search across KB articles, issues, ADR decisions, and session logs."""
        query_terms = [t.lower().strip() for t in query.split() if t.strip()]
        results: List[SearchResultItem] = []

        # 1. Search KB Articles
        for kb in self.collector.kb_articles:
            if tag and tag.lower() not in [t.lower() for t in kb.tags]:
                continue
            if entity_type and entity_type != "kb":
                continue

            score = self._compute_score(query_terms, kb.title, kb.tags, kb.body)
            if score > 0 or not query_terms:
                snippet = self._make_snippet(query_terms, kb.body)
                results.append(
                    SearchResultItem(
                        id=kb.id,
                        title=kb.title,
                        type="kb",
                        snippet=snippet,
                        file_path=kb.file_path,
                        score=score,
                        tags=kb.tags,
                    )
                )

        # 2. Search Issues
        for iss in self.collector.issues:
            if tag and tag.lower() not in [t.lower() for t in iss.tags]:
                continue
            if entity_type and entity_type != "issue":
                continue

            score = self._compute_score(query_terms, iss.title or iss.slug, iss.tags, iss.body or "")
            if score > 0 or not query_terms:
                snippet = self._make_snippet(query_terms, iss.body or "")
                results.append(
                    SearchResultItem(
                        id=iss.id,
                        title=iss.title or iss.slug,
                        type="issue",
                        snippet=snippet,
                        file_path=iss.file_path or "",
                        score=score,
                        tags=iss.tags,
                    )
                )

        # 3. Search Decisions (ADR)
        for dec in self.collector.decisions:
            if entity_type and entity_type != "decision":
                continue

            score = self._compute_score(query_terms, dec.title, [], dec.raw_markdown or "")
            if score > 0 or not query_terms:
                snippet = self._make_snippet(query_terms, dec.raw_markdown or "")
                results.append(
                    SearchResultItem(
                        id=dec.id,
                        title=f"{dec.id}: {dec.title}",
                        type="decision",
                        snippet=snippet,
                        file_path=".along/DECISIONS.md",
                        score=score,
                        tags=[dec.status],
                    )
                )

        # 4. Search Sessions
        for sess in self.collector.sessions:
            if entity_type and entity_type != "session":
                continue

            score = self._compute_score(query_terms, sess.summary or sess.slug, [], sess.body or "")
            if score > 0 or not query_terms:
                snippet = self._make_snippet(query_terms, sess.body or "")
                results.append(
                    SearchResultItem(
                        id=sess.id,
                        title=f"Session {sess.date}: {sess.summary or sess.slug}",
                        type="session",
                        snippet=snippet,
                        file_path=sess.file_path or "",
                        score=score,
                        tags=[sess.agent] if sess.agent else [],
                    )
                )

        # Sort by relevance score descending
        results.sort(key=lambda r: r.score, reverse=True)

        return SearchResponse(
            query=query,
            total=len(results),
            results=results,
        )

    def build_kb_graph(self) -> KBGraphSchema:
        """Build bidirectional link graph between KB articles and related topics/entities."""
        nodes: List[KBGraphNode] = []
        edges: List[KBGraphEdge] = []
        node_ids = set()

        # Add KB nodes
        for kb in self.collector.kb_articles:
            nodes.append(
                KBGraphNode(
                    id=kb.id,
                    label=kb.title,
                    type="kb",
                    category=kb.type,
                    tags=kb.tags,
                )
            )
            node_ids.add(kb.id)

        # Add links between KB articles and entities
        for kb in self.collector.kb_articles:
            for out in kb.outgoing_links:
                target_slug = out.strip().lower()
                # Find matching target
                target_id = None
                for candidate in self.collector.kb_articles:
                    if candidate.slug.lower() == target_slug or candidate.title.lower() == target_slug:
                        target_id = candidate.id
                        break
                if not target_id:
                    for iss in self.collector.issues:
                        if iss.slug.lower() == target_slug or iss.id.lower() == target_slug:
                            target_id = iss.id
                            if target_id not in node_ids:
                                nodes.append(
                                    KBGraphNode(
                                        id=iss.id,
                                        label=iss.title or iss.slug,
                                        type="issue",
                                        category=iss.type,
                                        tags=iss.tags,
                                    )
                                )
                                node_ids.add(target_id)
                            break

                if target_id:
                    edges.append(
                        KBGraphEdge(
                            source=kb.id,
                            target=target_id,
                            type="references",
                            label="links",
                        )
                    )

        return KBGraphSchema(nodes=nodes, edges=edges)

    def _compute_score(self, terms: List[str], title: str, tags: List[str], body: str) -> float:
        if not terms:
            return 1.0
        score = 0.0
        title_lower = title.lower()
        body_lower = body.lower()
        tags_lower = [t.lower() for t in tags]

        for term in terms:
            if term in title_lower:
                score += 10.0
            for tag in tags_lower:
                if term in tag:
                    score += 5.0
            # Count occurrences in body
            matches = body_lower.count(term)
            score += min(matches * 0.5, 5.0)

        return score

    def _make_snippet(self, terms: List[str], body: str) -> str:
        if not body:
            return ""
        if not terms:
            return body[:160].strip() + ("..." if len(body) > 160 else "")

        first_term = terms[0]
        pos = body.lower().find(first_term)
        if pos == -1:
            return body[:160].strip() + ("..." if len(body) > 160 else "")

        start = max(0, pos - 60)
        end = min(len(body), pos + 100)
        snippet = body[start:end].replace("\n", " ").strip()
        prefix = "..." if start > 0 else ""
        suffix = "..." if end < len(body) else ""
        return f"{prefix}{snippet}{suffix}"

