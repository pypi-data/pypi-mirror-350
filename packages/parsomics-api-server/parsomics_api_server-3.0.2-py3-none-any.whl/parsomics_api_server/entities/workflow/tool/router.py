from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.workflow.tool import (
    Tool,
    ToolPublic,
    ToolTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=Tool,
    transactions=ToolTransactions(),
)
router = APIRouter(
    prefix="/tool",
    tags=["workflow/tool"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/{key}", response_model=ToolPublic)
def get_tool(
    *,
    session: Session = Depends(get_session_ro),
    key: int,
):
    return _routing_helpers.get(session, key)


@router.post("/items/", response_model=list[ToolPublic])
def get_tools(
    *,
    session: Session = Depends(get_session_ro),
    keys: list[int],
):
    return _routing_helpers.get_batch(session, keys)


@router.get("/", response_model=list[ToolPublic])
def read_tools(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
