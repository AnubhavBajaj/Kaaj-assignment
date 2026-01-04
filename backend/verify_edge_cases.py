import asyncio
import logging
from app.database import AsyncSessionLocal
from app.models.business import Business, PersonalGuarantor, BusinessCredit, IndustryType
from app.models.loan import LoanRequest
from app.models.lender import Lender, LenderProgram, LenderCriteria, CriteriaType
from app.services.match_engine import MatchingEngine
from app.models.match import MatchResult
from sqlalchemy import select, delete

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_edge_cases():
    logger.info("\n--- Edge Case Verification ---")
    
    async with AsyncSessionLocal() as session:
        engine = MatchingEngine(session)

        # Cleanup existing test data
        test_lenders = ["Lender A", "Lender B", "Lender C"]
        lender_ids = (await session.execute(select(Lender.id).where(Lender.name.in_(test_lenders)))).scalars().all()
        if lender_ids:
            # Cleanup dependencies (MatchResult first)
            await session.execute(delete(MatchResult).where(MatchResult.lender_id.in_(lender_ids)))
            prog_ids = (await session.execute(select(LenderProgram.id).where(LenderProgram.lender_id.in_(lender_ids)))).scalars().all()
            if prog_ids:
                await session.execute(delete(LenderCriteria).where(LenderCriteria.program_id.in_(prog_ids)))
                await session.execute(delete(LenderProgram).where(LenderProgram.id.in_(prog_ids)))
            await session.execute(delete(Lender).where(Lender.id.in_(lender_ids)))
            await session.flush()

        # SETUP LENDERS
        # Lender A: Exclude NY State
        lender_a = Lender(name="Lender A", excluded_states=["NY"])
        session.add(lender_a)
        
        # Lender B: Exclude Retail Industry
        lender_b = Lender(name="Lender B", excluded_industries=["Retail"])
        session.add(lender_b)
        
        # Lender C: High FICO (700+)
        lender_c = Lender(name="Lender C")
        session.add(lender_c)
        await session.flush()
        
        prog_c = LenderProgram(lender_id=lender_c.id, program_name="Prime", tier_name="A")
        session.add(prog_c)
        await session.flush()
        
        session.add(LenderCriteria(program_id=prog_c.id, criteria_type=CriteriaType.FICO_MIN, value_numeric=700))
        await session.flush()
        
        # TEST CASE 1: Excluded State (NY)
        logger.info("\n1. Testing Excluded State (NY)...")
        b1 = Business(legal_name="NY Biz", industry=IndustryType.TECHNOLOGY, state="NY", years_in_business=3, annual_revenue=500000)
        session.add(b1)
        await session.flush()
        g1 = PersonalGuarantor(business_id=b1.id, first_name="A", last_name="B", fico_score=750, ownership_percentage=100)
        session.add(g1)
        session.add(BusinessCredit(business_id=b1.id)) # dummy
        l1 = LoanRequest(business_id=b1.id, amount=50000, term_months=24, equipment_age_years=2, equipment_type="Test Tech", equipment_cost=50000)
        session.add(l1)
        await session.commit() # Commit to persist IDs for query
        
        res1 = await engine.evaluate_application(l1.id)
        # Expect Lender A to fail (State), Lender B to pass, Lender C to pass
        for r in res1:
             lender_name = (await session.execute(select(Lender.name).where(Lender.id == r.lender_id))).scalar()
             logger.info(f"{lender_name}: Eligible={r.is_eligible}, Reasons={r.rejection_reasons}")
             if lender_name == "Lender A":
                 assert not r.is_eligible, "Lender A should fail NY business"
        
        # TEST CASE 2: Excluded Industry (Retail)
        logger.info("\n2. Testing Excluded Industry (Retail)...")
        b2 = Business(legal_name="Retail Biz", industry=IndustryType.RETAIL, state="TX", years_in_business=3, annual_revenue=500000)
        session.add(b2)
        await session.flush()
        g2 = PersonalGuarantor(business_id=b2.id, first_name="A", last_name="B", fico_score=750, ownership_percentage=100)
        session.add(g2)
        session.add(BusinessCredit(business_id=b2.id))
        l2 = LoanRequest(business_id=b2.id, amount=50000, term_months=24, equipment_age_years=2, equipment_type="Test Retail", equipment_cost=50000)
        session.add(l2)
        await session.commit()
        
        res2 = await engine.evaluate_application(l2.id)
        # Expect Lender B to fail
        for r in res2:
             lender_name = (await session.execute(select(Lender.name).where(Lender.id == r.lender_id))).scalar()
             logger.info(f"{lender_name}: Eligible={r.is_eligible}, Reasons={r.rejection_reasons}")
             if lender_name == "Lender B":
                 assert not r.is_eligible, "Lender B should fail Retail business"

        # TEST CASE 3: Low FICO
        logger.info("\n3. Testing Low FICO (600)...")
        b3 = Business(legal_name="Low FICO Biz", industry=IndustryType.TECHNOLOGY, state="TX", years_in_business=3, annual_revenue=500000)
        session.add(b3)
        await session.flush()
        g3 = PersonalGuarantor(business_id=b3.id, first_name="A", last_name="B", fico_score=600, ownership_percentage=100)
        session.add(g3)
        session.add(BusinessCredit(business_id=b3.id))
        l3 = LoanRequest(business_id=b3.id, amount=50000, term_months=24, equipment_age_years=2, equipment_type="Test FICO", equipment_cost=50000)
        session.add(l3)
        await session.commit()
        
        res3 = await engine.evaluate_application(l3.id)
        # Expect Lender C to fail
        for r in res3:
             lender_name = (await session.execute(select(Lender.name).where(Lender.id == r.lender_id))).scalar()
             logger.info(f"{lender_name}: Eligible={r.is_eligible}, Reasons={r.rejection_reasons}")
             if lender_name == "Lender C":
                 assert not r.is_eligible, "Lender C should fail FICO 600"

        logger.info("\nEdge Cases Verified Successfully.")

if __name__ == "__main__":
    asyncio.run(verify_edge_cases())
