from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.workflow.source import (
    Source,
    SourcePublic,
    SourceTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=Source,
    transactions=SourceTransactions(),
)
router = APIRouter(
    prefix="/source",
    tags=["workflow/source"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=SourcePublic)
def get_source(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[SourcePublic])
def get_sources(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[SourcePublic])
def read_sources(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
