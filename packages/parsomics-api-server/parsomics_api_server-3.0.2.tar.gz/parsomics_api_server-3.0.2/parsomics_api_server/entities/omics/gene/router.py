from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.omics.gene import (
    Gene,
    GenePublic,
    GeneTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=Gene,
    transactions=GeneTransactions(),
)
router = APIRouter(
    prefix="/gene",
    tags=["omics/gene"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=GenePublic)
def get_gene(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[GenePublic])
def get_genes(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[GenePublic])
def read_genes(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
