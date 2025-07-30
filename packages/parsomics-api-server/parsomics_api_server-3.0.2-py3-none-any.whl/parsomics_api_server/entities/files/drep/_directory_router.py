from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.files.drep import (
    DrepDirectory,
    DrepDirectoryPublic,
    DrepDirectoryTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers

_routing_helpers = RoutingHelpers(
    table_type=DrepDirectory,
    transactions=DrepDirectoryTransactions(),
)
router = APIRouter(
    prefix="/directory",
    tags=["files/drep/directory"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=DrepDirectoryPublic)
def get_directory(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[DrepDirectoryPublic])
def get_directories(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[DrepDirectoryPublic])
def read_directories(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
