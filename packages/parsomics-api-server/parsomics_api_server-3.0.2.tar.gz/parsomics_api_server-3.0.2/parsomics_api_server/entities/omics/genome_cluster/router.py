from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.omics.genome_cluster import (
    GenomeCluster,
    GenomeClusterPublic,
    GenomeClusterTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=GenomeCluster,
    transactions=GenomeClusterTransactions(),
)
router = APIRouter(
    prefix="/genome_cluster",
    tags=["omics/genome_cluster"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=GenomeClusterPublic)
def get_genome_cluster(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[GenomeClusterPublic])
def get_genome_clusters(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[GenomeClusterPublic])
def read_genome_clusters(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
