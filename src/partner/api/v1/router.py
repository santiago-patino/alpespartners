from fastapi import APIRouter
from .partner.router import router as partner_router


router = APIRouter()
router.include_router(partner_router, prefix="/partner", tags=["Partner"])