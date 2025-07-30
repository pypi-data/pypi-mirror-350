from fastapi import APIRouter

from ._file_router import router as file_router
from ._entry_router import router as entry_router

router = APIRouter(
    prefix="/gene_annotation",
)

router.include_router(file_router)
router.include_router(entry_router)
