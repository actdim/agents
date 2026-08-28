"""Cytoscape DAG and Entity Dependency Graph Builder."""

from typing import Dict, Any, List


def build_entity_dag_graph(collector) -> Dict[str, Any]:
    """Construct Cytoscape-compatible JSON graph structure of entities and dependencies."""
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    seen_nodes = set()

    # 1. Add Issue nodes
    for iss in collector.issues:
        node_id = iss.id
        if node_id in seen_nodes:
            continue
        seen_nodes.add(node_id)
        nodes.append({
            "id": node_id,
            "label": iss.title or iss.slug,
            "type": "issue",
            "issue_type": iss.type,
            "status": iss.status,
            "priority": iss.priority,
            "slug": iss.slug,
            "file_path": iss.file_path,
        })

    # 2. Add Milestone nodes
    for m in collector.milestones:
        node_id = m.id
        if node_id in seen_nodes:
            continue
        seen_nodes.add(node_id)
        nodes.append({
            "id": node_id,
            "label": m.title or m.slug,
            "type": "milestone",
            "status": m.status,
            "progress_pct": m.progress_pct,
            "slug": m.slug,
            "file_path": m.file_path,
        })

    # 3. Add Risk nodes
    for r in collector.risks:
        node_id = r.id
        if node_id in seen_nodes:
            continue
        seen_nodes.add(node_id)
        nodes.append({
            "id": node_id,
            "label": r.title or r.slug,
            "type": "risk",
            "severity": r.severity,
            "status": r.status,
            "slug": r.slug,
            "file_path": r.file_path,
        })

    # 4. Add Edges
    # A. Issue blocked_by edges
    for iss in collector.issues:
        for blocker in iss.blocked_by:
            # Resolve canonical blocker id
            target_id = None
            if "--" in blocker:
                target_id = blocker
            else:
                for candidate in collector.issues:
                    if candidate.slug == blocker:
                        target_id = candidate.id
                        break
            if target_id and target_id in seen_nodes:
                edges.append({
                    "source": target_id,
                    "target": iss.id,
                    "type": "blocks",
                    "label": "blocks",
                })

    # B. Milestone target_issues / issue milestone relations
    for iss in collector.issues:
        if iss.milestone:
            m_id = f"milestone--{iss.milestone}"
            if m_id in seen_nodes:
                edges.append({
                    "source": iss.id,
                    "target": m_id,
                    "type": "belongs_to",
                    "label": "in milestone",
                })

    for m in collector.milestones:
        for target_key in m.target_issues:
            target_id = None
            if "--" in target_key:
                target_id = target_key
            else:
                for candidate in collector.issues:
                    if candidate.slug == target_key:
                        target_id = candidate.id
                        break
            if target_id and target_id in seen_nodes:
                # Check if already added
                if not any(e["source"] == target_id and e["target"] == m.id for e in edges):
                    edges.append({
                        "source": target_id,
                        "target": m.id,
                        "type": "belongs_to",
                        "label": "target",
                    })

    # C. Parent-child relationships
    for iss in collector.issues:
        if iss.parent:
            parent_id = iss.parent if "--" in iss.parent else f"feat--{iss.parent}"
            if parent_id in seen_nodes:
                edges.append({
                    "source": parent_id,
                    "target": iss.id,
                    "type": "parent_of",
                    "label": "child",
                })

    return {"nodes": nodes, "edges": edges}

