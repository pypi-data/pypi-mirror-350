from fastapi import APIRouter

from ._directory_router import router as directory_router
from ._entry_router import router as entry_router

router = APIRouter(
    prefix="/drep",
)

router.include_router(directory_router)
router.include_router(entry_router)
