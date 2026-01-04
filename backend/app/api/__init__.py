"""API routes for the loan underwriting platform."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def api_root():
    """API v1 root endpoint."""
    return {"message": "Loan Underwriting API v1"}


# Import and include sub-routers here as they are created
# from app.api.loans import router as loans_router
# from app.api.applications import router as applications_router
# from app.api.documents import router as documents_router

# router.include_router(loans_router, prefix="/loans", tags=["loans"])
# router.include_router(applications_router, prefix="/applications", tags=["applications"])
# router.include_router(documents_router, prefix="/documents", tags=["documents"])
