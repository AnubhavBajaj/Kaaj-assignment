from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.business import Business
from app.models.loan import LoanRequest
from app.models.lender import Lender, LenderProgram, LenderCriteria, CriteriaType
from app.models.match import MatchResult
from app.services.evaluators.registry import EVALUATOR_REGISTRY
import logging

logger = logging.getLogger(__name__)

class MatchingEngine:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def evaluate_application(self, loan_request_id: str) -> List[MatchResult]:
        """
        Main entry point to evaluate a loan request against all active lenders.
        """
        # 1. Load Data
        loan_request = await self._load_loan_request_data(loan_request_id)
        if not loan_request:
            logger.error(f"Loan request {loan_request_id} not found.")
            return []
        
        # Prepare data dict for evaluators
        application_data = {
            "loan_request": loan_request,
            "business": loan_request.business,
            "credit_profile": loan_request.business.credit_profile,
            "guarantors": loan_request.business.guarantors
        }

        # 2. Load Active Lenders
        lenders = await self._load_active_lenders()
        
        results = []

        # 3. Iterate and Evaluate
        for lender in lenders:
            # First check lender-level exclusions (Industry/State)
            # These are stored on Lender model, so we can check them manually or use evaluators with mapped keys
            lender_passed, lender_rejection = self._check_lender_exclusions(lender, application_data)
            
            if not lender_passed:
                # Store rejection for lender (no specific program)
                results.append(MatchResult(
                    loan_request_id=loan_request.id,
                    lender_id=lender.id,
                    is_eligible=False,
                    fit_score=0,
                    rejection_reasons=[lender_rejection]
                ))
                continue

            for program in lender.programs:
                match_result = self._evaluate_program(program, lender, application_data)
                results.append(match_result)

        # 4. Save Results
        for res in results:
            self.session.add(res)
        await self.session.commit()
        
        # Return sorted by score
        results.sort(key=lambda x: x.fit_score, reverse=True)
        return results

    async def _load_loan_request_data(self, loan_id: str) -> LoanRequest:
        stmt = select(LoanRequest).where(LoanRequest.id == loan_id).options(
            selectinload(LoanRequest.business).selectinload(Business.credit_profile),
            selectinload(LoanRequest.business).selectinload(Business.guarantors)
        )
        return (await self.session.execute(stmt)).scalars().first()

    async def _load_active_lenders(self) -> List[Lender]:
        stmt = select(Lender).where(Lender.is_active == True).options(
            selectinload(Lender.programs).selectinload(LenderProgram.criteria)
        )
        return (await self.session.execute(stmt)).scalars().all()

    def _check_lender_exclusions(self, lender: Lender, app_data: Dict) -> (bool, str):
        # Check State
        if lender.excluded_states:
             evaluator = EVALUATOR_REGISTRY.get("STATE_EXCLUDED")()
             res = evaluator.evaluate(app_data, lender.excluded_states)
             if not res.passed:
                 return False, res.reason
        
        # Check Industry
        if lender.excluded_industries:
             evaluator = EVALUATOR_REGISTRY.get(CriteriaType.INDUSTRY_EXCLUDED)()
             res = evaluator.evaluate(app_data, lender.excluded_industries)
             if not res.passed:
                 return False, res.reason

        return True, ""

    def _evaluate_program(self, program: LenderProgram, lender: Lender, app_data: Dict) -> MatchResult:
        score = 100
        reasons = []
        is_eligible = True
        
        criteria_details = {}

        for criterion in program.criteria:
            evaluator_cls = EVALUATOR_REGISTRY.get(criterion.criteria_type)
            if not evaluator_cls:
                logger.warning(f"No evaluator for {criterion.criteria_type}")
                continue
            
            evaluator = evaluator_cls()
            
            # Helper to get value (numeric, text, or bool)
            val = criterion.value_numeric if criterion.value_numeric is not None else (
                criterion.value_text if criterion.value_text else criterion.value_boolean
            )
            
            result = evaluator.evaluate(app_data, val)
            
            criteria_details[criterion.criteria_type.value] = {
                "passed": result.passed,
                "reason": result.reason,
                "impact": result.score_impact
            }

            score += result.score_impact
            
            if not result.passed:
                is_eligible = False
                reasons.append(result.reason)

        # Cap score
        score = max(0, min(100, score))
        if not is_eligible:
             score = 0 # Or keep score but mark valid=False? User req says 0 implies ineligible usually.
                       # But prompt says "Critical failures... ineligible", "Major failures... -40 points".
                       # If major failure drops score to 60, is it ineligible?
                       # Usually yes if it fails a HARD criteria.
                       # For now, let's assume ALL criteria are hard requirements for eligibility,
                       # but score reflects "strength" of application.
                       


        return MatchResult(
            loan_request_id=app_data["loan_request"].id,
            lender_id=lender.id,
            program_id=program.id,
            is_eligible=is_eligible,
            fit_score=score if is_eligible else 0,
            rejection_reasons=reasons,
            criteria_details=criteria_details
        )
