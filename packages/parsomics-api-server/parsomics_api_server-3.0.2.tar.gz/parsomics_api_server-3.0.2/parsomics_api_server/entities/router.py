from fastapi import APIRouter

from .workflow.router import router as workflow_router
from .files.router import router as files_router
from .omics.router import router as omics_router

router = APIRouter(
    prefix="/entities",
)

router.include_router(workflow_router)
router.include_router(files_router)
router.include_router(omics_router)
