"""Metrics and Full Dashboard Data API endpoints."""

from fastapi import APIRouter, Depends
from ..schemas.metrics import DashboardMetricsSchema, FullDashboardDataSchema
from ..core.collector import EntityCollector

router = APIRouter(tags=["Metrics & Data"])


def get_collector() -> EntityCollector:
    raise NotImplementedError


@router.get("/metrics", response_model=DashboardMetricsSchema, summary="Get dashboard metrics")
def get_metrics(collector: EntityCollector = Depends(get_collector)):
    collector.collect_all()
    return collector.metrics


@router.get("/data", response_model=FullDashboardDataSchema, summary="Get full combined dashboard dataset")
def get_full_data(collector: EntityCollector = Depends(get_collector)):
    collector.collect_all()
    return collector.to_full_data()


@router.get("/graph", summary="Get entity DAG dependency graph for Cytoscape")
def get_dag_graph(collector: EntityCollector = Depends(get_collector)):
    collector.collect_all()
    from ..core.graph import build_entity_dag_graph
    return build_entity_dag_graph(collector)

