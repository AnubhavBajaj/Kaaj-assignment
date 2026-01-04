from typing import List, Optional, Any
from uuid import UUID
from pydantic import Field
from app.models.lender import CriteriaType
from app.schemas.base import ORMModel

# Criteria
class LenderCriteriaBase(ORMModel):
    criteria_type: CriteriaType
    value_numeric: Optional[float] = None
    value_text: Optional[str] = None
    value_boolean: Optional[bool] = None

class LenderCriteriaCreate(LenderCriteriaBase):
    pass

class LenderCriteriaResponse(LenderCriteriaBase):
    id: UUID
    program_id: UUID

# Program
class LenderProgramBase(ORMModel):
    program_name: str
    tier_name: Optional[str] = None

class LenderProgramCreate(LenderProgramBase):
    criteria: List[LenderCriteriaCreate] = []

class LenderProgramResponse(LenderProgramBase):
    id: UUID
    lender_id: UUID
    criteria: List[LenderCriteriaResponse] = []

# Lender
class LenderBase(ORMModel):
    name: str
    is_active: bool = True
    excluded_states: List[str] = []
    excluded_industries: List[str] = []
    excluded_equipment_types: List[str] = []

class LenderCreate(LenderBase):
    programs: List[LenderProgramCreate] = []

class LenderUpdate(ORMModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    excluded_states: Optional[List[str]] = None
    excluded_industries: Optional[List[str]] = None
    excluded_equipment_types: Optional[List[str]] = None

class LenderResponse(LenderBase):
    id: UUID
    programs: List[LenderProgramResponse] = []
    program_count: Optional[int] = None # For list view
