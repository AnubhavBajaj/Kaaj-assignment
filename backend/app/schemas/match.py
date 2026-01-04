from typing import List, Dict, Optional, Any
from uuid import UUID
from app.schemas.base import ORMModel
from app.schemas.lender import LenderResponse, LenderProgramResponse

class MatchCriteriaDetail(ORMModel):
    passed: bool
    reason: Optional[str] = None
    impact: int

class MatchResultResponse(ORMModel):
    id: UUID
    loan_request_id: UUID
    lender_id: UUID
    program_id: Optional[UUID] = None
    
    is_eligible: bool
    fit_score: int
    rejection_reasons: List[str] = []
    criteria_details: Optional[Dict[str, Any]] = {} # Map of criteria_type -> details
    
    # Nested for convenience
    lender: Optional[LenderResponse] = None
    program: Optional[LenderProgramResponse] = None
