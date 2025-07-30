from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.workflow.assembly import (
    Assembly,
    AssemblyPublic,
    AssemblyTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=Assembly,
    transactions=AssemblyTransactions(),
)
router = APIRouter(
    prefix="/assembly",
    tags=["workflow/assembly"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=AssemblyPublic)
def get_assembly(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[AssemblyPublic])
def get_assemblies(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[AssemblyPublic])
def read_assemblies(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
