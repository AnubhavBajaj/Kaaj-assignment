from typing import List, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.services.match_engine import MatchingEngine
from app.models.match import MatchResult
from app.models.loan import LoanRequest
from app.models.lender import Lender, LenderProgram
from app.schemas.match import MatchResultResponse

router = APIRouter(prefix="/underwriting", tags=["Underwriting"])

@router.post("/run/{application_id}", status_code=status.HTTP_200_OK)
async def run_underwriting(application_id: UUID, db: AsyncSession = Depends(get_db)):
    # Verify Application Exists
    stmt = select(LoanRequest).where(LoanRequest.id == application_id)
    result = await db.execute(stmt)
    loan = result.scalars().first()
    
    if not loan:
        raise HTTPException(status_code=404, detail="Application not found")

    # Run Matching Engine (Inline for now, can be moved to BackgroundTasks/Celery)
    # Note: MatchingEngine handles session commit internally for results
    engine = MatchingEngine(db)
    
    # Prune old results first? match_engine appends, so we might duplicate if we re-run.
    # verify_matching.py showed appending. logic says "Save Results". 
    # It does not delete old ones in provided code. 
    # Valid usage implies we should clear old results for this app before running again to avoid dupes.
    # I'll add a delete step here for safety.
    
    stmt_del = select(MatchResult).where(MatchResult.loan_request_id == application_id)
    # sqlalchemy delete is usually: delete(MatchResult).where(...)
    # but to include in session we execute the delete statement
    from sqlalchemy import delete
    await db.execute(delete(MatchResult).where(MatchResult.loan_request_id == application_id))
    # match_engine commits, so we should probably commit this delete or let match engine handle it.
    # match_engine calls commit() at the end.
    # If I execute delete here, it's in the transaction. 
    # Passing session to engine... engine writes and commits.
    # So if I wait, it should be fine.
    
    match_results = await engine.evaluate_application(str(application_id))
    
    return {
        "job_id": str(application_id), # Using app ID as job ID for this synchronous implementation
        "status": "completed",
        "matches_found": len(match_results)
    }

@router.get("/results/{application_id}", response_model=List[MatchResultResponse])
async def get_underwriting_results(application_id: UUID, db: AsyncSession = Depends(get_db)):
    # Results should include Lender and Program details
    stmt = select(MatchResult).where(MatchResult.loan_request_id == application_id).options(
        selectinload(MatchResult.lender).selectinload(Lender.programs).selectinload(LenderProgram.criteria),
        selectinload(MatchResult.program).selectinload(LenderProgram.criteria)
    ).order_by(MatchResult.fit_score.desc())
    
    result = await db.execute(stmt)
    matches = result.scalars().all()
    
    return matches
