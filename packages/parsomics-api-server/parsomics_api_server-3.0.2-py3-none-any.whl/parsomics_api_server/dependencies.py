from sqlmodel import Session
from parsomics_core.globals.database import engine_ro


def get_session_ro():
    with Session(engine_ro) as session:
        yield session
