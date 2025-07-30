from typing import Any

from fastapi import HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select


class RoutingHelpers(BaseModel):
    table_type: type
    transactions: Any

    def get_batch(self, session: Session, keys: list[int]):
        reads = session.exec(
            select(self.table_type).where(self.table_type.key.in_(keys))
        ).all()
        if not reads:
            raise HTTPException(
                status_code=404,
                detail=f"{self.table_type.__name__} entries with keys {keys} not found",
            )
        return reads

    def get(self, session: Session, key: int):
        read = session.get(self.table_type, key)
        if read is None:
            raise HTTPException(
                status_code=404,
                detail=f"{self.table_type.__name__} entry with key {key} not found",
            )
        return read

    def read(
        self,
        session: Session,
        offset: int = 0,
        limit: int = Query(default=100, le=100),
    ):
        statement = select(self.table_type).offset(offset).limit(limit)
        reads = session.exec(statement).all()
        if not reads:
            raise HTTPException(
                status_code=404,
                detail=f"{self.table_type.__name__} entries not found",
            )
        return reads
