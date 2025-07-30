from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.files.gff import (
    GFFFile,
    GFFFilePublic,
    GFFFileTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=GFFFile,
    transactions=GFFFileTransactions(),
)
router = APIRouter(
    prefix="/file",
    tags=["files/gff/file"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=GFFFilePublic)
def get_file(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[GFFFilePublic])
def get_files(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[GFFFilePublic])
def read_files(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
