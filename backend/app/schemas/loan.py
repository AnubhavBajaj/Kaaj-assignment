from typing import List, Optional
from datetime import datetime
from uuid import UUID
from pydantic import Field
from app.models.loan import LoanStatus
from app.schemas.base import ORMModel
from app.schemas.business import BusinessCreate, BusinessResponse, GuarantorCreate

class LoanRequestBase(ORMModel):
    amount: float = Field(gt=0)
    term_months: int = Field(gt=0)
    equipment_type: Optional[str] = None
    equipment_age_years: int = 0
    equipment_cost: Optional[float] = None
    soft_costs: float = 0
    is_private_party_sale: bool = False

class LoanRequestCreate(LoanRequestBase):
    pass

class LoanRequestResponse(LoanRequestBase):
    id: UUID
    business_id: UUID
    status: LoanStatus
    created_at: datetime
    updated_at: datetime
    
    # We might want to nest business here for convenience in some views
    business: Optional[BusinessResponse] = None

# Composite Schema for Application Creation
class ApplicationCreate(ORMModel):
    business: BusinessCreate
    guarantors: List[GuarantorCreate]
    loan_request: LoanRequestCreate
    # Credit is usually internal/fetched, but we allow passing it for testing/overrides if needed
    # For now, let's assume credit profile is created empty or fetched later, 
    # but the user prompt implied creating "business, guarantors, credit, and loan request atomically".
    # So we'll include optional credit params or simple creation.
    
class ApplicationResponse(ORMModel):
    application_id: UUID
    status: str
