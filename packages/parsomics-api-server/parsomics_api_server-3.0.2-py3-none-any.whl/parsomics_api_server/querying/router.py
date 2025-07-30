from typing import Any
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy.engine.row import Row

from parsomics_api_server.dependencies import get_session_ro
from parsomics_api_server.querying._model_registry import model_registry
from sqlmodel_query_builder import QueryArgs, QueryBuilder

builder = QueryBuilder(mdl_registry=model_registry)

router = APIRouter(
    prefix="/querying",
)


@router.post("/", response_model=Any)
def query(
    *,
    session: Session = Depends(get_session_ro),
    query_args: QueryArgs,
):
    statement = builder.build_statement(query_args)
    results = session.exec(statement).all()

    # Convert SQLAlchemy rows to tuples, which are serializable
    results = [tuple(r) if isinstance(r, Row) else r for r in results]

    return results
