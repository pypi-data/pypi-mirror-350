from fastapi import APIRouter

from .contig.router import router as contig_router
from .fragment.router import router as fragment_router
from .fragment_protein_link.router import router as fragment_protein_link_router
from .gene.router import router as gene_router
from .genome.router import router as genome_router
from .genome_cluster.router import router as genome_cluster_router
from .protein.router import router as protein_router
from .repeated_region.router import router as repeated_region_router
from .sample.router import router as sample_router

router = APIRouter(
    prefix="/omics",
)

router.include_router(contig_router)
router.include_router(fragment_router)
router.include_router(fragment_protein_link_router)
router.include_router(gene_router)
router.include_router(genome_router)
router.include_router(genome_cluster_router)
router.include_router(protein_router)
router.include_router(repeated_region_router)
router.include_router(sample_router)
