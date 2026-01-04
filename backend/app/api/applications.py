from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.business import Business, PersonalGuarantor, BusinessCredit
from app.models.loan import LoanRequest, LoanStatus
from app.schemas.loan import ApplicationCreate, ApplicationResponse, LoanRequestResponse
from app.schemas.business import BusinessResponse

router = APIRouter(prefix="/applications", tags=["Applications"])

@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(app_data: ApplicationCreate, db: AsyncSession = Depends(get_db)):
    # 1. atomic creation logic
    # Create Business
    business = Business(
        legal_name=app_data.business.legal_name,
        dba_name=app_data.business.dba_name,
        industry=app_data.business.industry,
        state=app_data.business.state,
        years_in_business=app_data.business.years_in_business,
        annual_revenue=app_data.business.annual_revenue
    )
    db.add(business)
    await db.flush() # get ID

    # Create Guarantors
    for g_data in app_data.guarantors:
        guarantor = PersonalGuarantor(
            business_id=business.id,
            **g_data.model_dump()
        )
        db.add(guarantor)

    # Create Credit Profile (Default empty if not provided logic, or use basic defaults from model)
    # The schema doesn't force credit input, so we create a default one to attach scores later if needed
    credit = BusinessCredit(business_id=business.id)
    db.add(credit)

    # Create Loan Request
    loan_request = LoanRequest(
        business_id=business.id,
        **app_data.loan_request.model_dump()
    )
    loan_request.status = LoanStatus.DRAFT
    db.add(loan_request)
    
    await db.commit()
    await db.refresh(loan_request)

    return ApplicationResponse(application_id=loan_request.id, status=loan_request.status.value)

@router.get("/", response_model=List[LoanRequestResponse])
async def list_applications(
    status: LoanStatus = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(LoanRequest).offset(skip).limit(limit).order_by(LoanRequest.created_at.desc())
    
    if status:
        stmt = stmt.where(LoanRequest.status == status)
    
    # Eager load business and its nested relations for response
    stmt = stmt.options(
        selectinload(LoanRequest.business).selectinload(Business.guarantors),
        selectinload(LoanRequest.business).selectinload(Business.credit_profile)
    )
    
    result = await db.execute(stmt)
    return result.scalars().all()

@router.get("/{id}", response_model=LoanRequestResponse)
async def get_application(id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(LoanRequest).where(LoanRequest.id == id).options(
        selectinload(LoanRequest.business).selectinload(Business.guarantors),
        selectinload(LoanRequest.business).selectinload(Business.credit_profile)
    )
    result = await db.execute(stmt)
    loan = result.scalars().first()
    
    if not loan:
        raise HTTPException(status_code=404, detail="Application not found")
        
    return loan

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(LoanRequest).where(LoanRequest.id == id)
    result = await db.execute(stmt)
    loan = result.scalars().first()
    
    if not loan:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Soft Delete logic implies converting status to specific 'DELETED' or similar?
    # Or strict delete? User requested "Soft delete (set status = DELETED)"
    # I need to ensure LoanStatus has DELETED.
    # Assuming LoanStatus enum has DELETED (it doesn't yet, assume DRAFT/SUBMITTED...). 
    # Checking LoanStatus definition...
    # If not, I will add it or just hard delete for now if enum is restricted.
    # Actually wait, Enum in app/models/loan.py: DRAFT, SUBMITTED, APPROVED, DECLINED, FUNDED. 
    # I should add DELETED or CANCELLED.
    # For now, I'll delete the record properly or check if I can modify Enum.
    # Modifying Postgres Enum in Alembic is annoying.
    # I'll stick to hard delete for now or 'DECLINED' as placeholder if safer, 
    # but actual DELETE verb usually implies removal. 
    # Or I can use a separate is_deleted flag if models allow.
    # Let's check model... LoanRequest has status.
    # I'll modify the delete to just delete for now to be simple unless I see a DELETED status.
    
    # Soft Delete implementation
    loan.status = LoanStatus.DELETED
    await db.commit()
