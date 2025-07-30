from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.workflow.metadata import (
    Metadata,
    MetadataPublic,
    MetadataTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=Metadata,
    transactions=MetadataTransactions(),
)
router = APIRouter(
    prefix="/metadata",
    tags=["workflow/metadata"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/item/", response_model=MetadataPublic)
def get_metadata(
    *,
    session: Session = Depends(get_session_ro),
):
    METADATA_KEY: int = 1
    return _routing_helpers.get(session, METADATA_KEY)
