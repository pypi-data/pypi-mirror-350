from fastapi import APIRouter

from .drep.router import router as drep_router
from .fasta.router import router as fasta_router
from .gff.router import router as gff_router
from .gene_annotation.router import router as gene_annotation_router
from .gtdbtk.router import router as gtdbtk_router
from .protein_annotation.router import router as protein_annotation_router

router = APIRouter(
    prefix="/files",
)

router.include_router(fasta_router)
router.include_router(gff_router)
router.include_router(drep_router)
router.include_router(gene_annotation_router)
router.include_router(gtdbtk_router)
router.include_router(protein_annotation_router)
