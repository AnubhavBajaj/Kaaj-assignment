from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.lender import Lender, LenderProgram, LenderCriteria
from app.schemas.lender import (
    LenderCreate, 
    LenderResponse, 
    LenderUpdate,
    LenderProgramCreate,
    LenderCriteriaCreate
)

router = APIRouter(prefix="/lenders", tags=["Lenders"])

@router.get("/", response_model=List[LenderResponse])
async def list_lenders(db: AsyncSession = Depends(get_db)):
    stmt = select(Lender).options(
        selectinload(Lender.programs).selectinload(LenderProgram.criteria)
    ).order_by(Lender.name)
    result = await db.execute(stmt)
    lenders = result.scalars().all()
    
    # We might want summary stats but schema expects full list for now.
    # Program count should be calculated.
    resp = []
    for l in lenders:
        l_resp = LenderResponse.model_validate(l)
        l_resp.program_count = len(l.programs)
        resp.append(l_resp)
        
    return resp

@router.get("/{id}", response_model=LenderResponse)
async def get_lender(id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Lender).where(Lender.id == id).options(
        selectinload(Lender.programs).selectinload(LenderProgram.criteria)
    )
    result = await db.execute(stmt)
    lender = result.scalars().first()
    
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found")
        
    l_resp = LenderResponse.model_validate(lender)
    l_resp.program_count = len(lender.programs)
    return l_resp

@router.post("/", response_model=LenderResponse, status_code=status.HTTP_201_CREATED)
async def create_lender(lender_data: LenderCreate, db: AsyncSession = Depends(get_db)):
    # Create Lender
    lender = Lender(
        name=lender_data.name,
        is_active=lender_data.is_active,
        excluded_states=lender_data.excluded_states,
        excluded_industries=lender_data.excluded_industries,
        excluded_equipment_types=lender_data.excluded_equipment_types
    )
    db.add(lender)
    await db.flush()
    
    # Create Programs & Criteria
    for prog_data in lender_data.programs:
        program = LenderProgram(
            lender_id=lender.id,
            program_name=prog_data.program_name,
            tier_name=prog_data.tier_name
        )
        db.add(program)
        await db.flush()
        
        for crit_data in prog_data.criteria:
            criteria = LenderCriteria(
                program_id=program.id,
                criteria_type=crit_data.criteria_type,
                value_numeric=crit_data.value_numeric,
                value_text=crit_data.value_text,
                value_boolean=crit_data.value_boolean
            )
            db.add(criteria)
            
    await db.commit()
    # Reload with relations
    return await get_lender(lender.id, db)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lender(id: UUID, db: AsyncSession = Depends(get_db)):
    stmt = select(Lender).where(Lender.id == id)
    result = await db.execute(stmt)
    lender = result.scalars().first()
    
    if not lender:
        raise HTTPException(status_code=404, detail="Lender not found")
        
    # Soft delete as requested
    lender.is_active = False
    await db.commit()

@router.put("/{lender_id}/programs/{program_id}/criteria", response_model=LenderResponse)
async def update_program_criteria(
    lender_id: UUID,
    program_id: UUID,
    criteria_list: List[LenderCriteriaCreate],
    db: AsyncSession = Depends(get_db)
):
    # 1. Verify existence
    stmt = select(LenderProgram).where(LenderProgram.id == program_id, LenderProgram.lender_id == lender_id)
    program = (await db.execute(stmt)).scalars().first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
        
    # 2. Delete existing criteria (simplest update strategy for criteria list)
    # Get current criteria
    stmt_del = select(LenderCriteria).where(LenderCriteria.program_id == program_id)
    existing_criteria = (await db.execute(stmt_del)).scalars().all()
    for crit in existing_criteria:
        await db.delete(crit)
        
    # 3. Add new
    for crit_data in criteria_list:
        criteria = LenderCriteria(
            program_id=program_id,
            criteria_type=crit_data.criteria_type,
            value_numeric=crit_data.value_numeric,
            value_text=crit_data.value_text,
            value_boolean=crit_data.value_boolean
        )
        db.add(criteria)
        
    await db.commit()
    return await get_lender(lender_id, db)
