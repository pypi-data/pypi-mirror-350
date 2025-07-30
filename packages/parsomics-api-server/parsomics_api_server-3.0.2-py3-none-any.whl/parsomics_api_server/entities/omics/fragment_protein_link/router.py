from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from parsomics_core.entities.omics.fragment_protein_link import (
    FragmentProteinLink,
    FragmentProteinLinkPublic,
    FragmentProteinLinkTransactions,
)

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.entities._helpers import RoutingHelpers


_routing_helpers = RoutingHelpers(
    table_type=FragmentProteinLink,
    transactions=FragmentProteinLinkTransactions(),
)
router = APIRouter(
    prefix="/fragment_protein_link",
    tags=["omics/fragment_protein_link"],
    responses={
        404: {"description": "Not found"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/", response_model=list[FragmentProteinLinkPublic])
def read_fragment_protein_links(
    *,
    session: Session = Depends(get_session_ro),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return _routing_helpers.read(session, offset, limit)
