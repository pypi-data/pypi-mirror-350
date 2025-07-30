from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.omics.genome import (
    Genome,
    GenomePublic,
    GenomeTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=Genome,
    transactions=GenomeTransactions(),
)
router = APIRouter(
    prefix="/genome",
    tags=["omics/genome"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=GenomePublic)
def get_genome(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[GenomePublic])
def get_genomes(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[GenomePublic])
def read_genomes(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
