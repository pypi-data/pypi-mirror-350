from fastapi import APIRouter

from .project.router import router as project_router
from .run.router import router as run_router
from .source.router import router as source_router
from .tool.router import router as tool_router
from .assembly.router import router as assembly_router
from .metadata.router import router as metadata_router

router = APIRouter(
    prefix="/workflow",
)

router.include_router(project_router)
router.include_router(run_router)
router.include_router(source_router)
router.include_router(tool_router)
router.include_router(assembly_router)
router.include_router(metadata_router)
