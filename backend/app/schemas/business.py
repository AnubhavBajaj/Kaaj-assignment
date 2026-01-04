from typing import List, Optional
from datetime import date, datetime
from uuid import UUID
from pydantic import Field, field_validator
from app.models.business import IndustryType
from app.schemas.base import ORMModel

# Guarantor Schemas
class GuarantorBase(ORMModel):
    first_name: str
    last_name: str
    fico_score: int = Field(ge=300, le=850)
    ownership_percentage: float = Field(gt=0, le=100)
    has_bankruptcy: bool = False
    bankruptcy_discharge_date: Optional[date] = None
    has_foreclosure: bool = False
    has_repossession: bool = False
    has_judgement: bool = False
    revolving_debt_balance: float = 0
    total_unsecured_debt: float = 0

class GuarantorCreate(GuarantorBase):
    pass

class GuarantorResponse(GuarantorBase):
    id: UUID
    business_id: UUID

# Credit Profile Schemas
class BusinessCreditBase(ORMModel):
    paynet_score: Optional[int] = None
    has_comparable_credit: bool = False
    comparable_credit_amount: float = 0
    open_trade_lines_count: int = 0
    has_collections: bool = False
    has_tax_liens: bool = False
    collections_charge_off_date: Optional[date] = None

class BusinessCreditCreate(BusinessCreditBase):
    pass

class BusinessCreditResponse(BusinessCreditBase):
    id: UUID
    business_id: UUID

# Business Schemas
class BusinessBase(ORMModel):
    legal_name: str
    dba_name: Optional[str] = None
    industry: IndustryType
    state: str = Field(min_length=2, max_length=2)
    years_in_business: float
    annual_revenue: float

    @field_validator('state')
    @classmethod
    def validate_state(cls, v: str) -> str:
        return v.upper()

class BusinessCreate(BusinessBase):
    pass

class BusinessResponse(BusinessBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    guarantors: List[GuarantorResponse] = []
    credit_profile: Optional[BusinessCreditResponse] = None
