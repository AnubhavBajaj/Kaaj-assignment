import asyncio
import logging
from app.database import AsyncSessionLocal
from app.models.business import Business, PersonalGuarantor, BusinessCredit, IndustryType
from app.models.loan import LoanRequest
from app.models.lender import Lender, LenderProgram, LenderCriteria, CriteriaType
from app.models.match import MatchResult
from app.services.match_engine import MatchingEngine
from sqlalchemy import select, delete

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_matching():
    logger.info("Starting Matching Engine verification...")
    
    async with AsyncSessionLocal() as session:
        engine = MatchingEngine(session)

        # Cleanup existing test data
        test_lenders = ["Match Lender", "Fail Industry", "Fail FICO"]
        
        # 0. Get IDs
        lender_ids = (await session.execute(select(Lender.id).where(Lender.name.in_(test_lenders)))).scalars().all()
        
        if lender_ids:
            # 1. Delete Dependencies
            await session.execute(delete(MatchResult).where(MatchResult.lender_id.in_(lender_ids)))
            
            prog_ids = (await session.execute(select(LenderProgram.id).where(LenderProgram.lender_id.in_(lender_ids)))).scalars().all()
            if prog_ids:
                await session.execute(delete(LenderCriteria).where(LenderCriteria.program_id.in_(prog_ids)))
                await session.execute(delete(LenderProgram).where(LenderProgram.id.in_(prog_ids)))
                
            await session.execute(delete(Lender).where(Lender.id.in_(lender_ids)))
            await session.flush()

        # 1. Setup Mock Data
        # Business
        business = Business(
            legal_name="Test Business LLC",
            industry=IndustryType.CONSTRUCTION, # Use Enum
            state="TX",
            years_in_business=5,
            annual_revenue=1_000_000
        )
        session.add(business)
        await session.flush()
        
        # Guarantor (Good FICO)
        guarantor = PersonalGuarantor(
            business_id=business.id,
            first_name="John",
            last_name="Doe",
            fico_score=750,
            ownership_percentage=100
        )
        session.add(guarantor)
        
        # Credit
        credit = BusinessCredit(
            business_id=business.id,
            paynet_score=700,
            comparable_credit_amount=50_000
        )
        session.add(credit)
        
        # Loan Request
        loan = LoanRequest(
            business_id=business.id,
            amount=100_000,
            term_months=36,
            equipment_type="Excavator",
            equipment_cost=100_000,
            equipment_age_years=2
        )
        session.add(loan)
        await session.flush()
        
        # Lender 1: Matches (Construction allowed, FICO 700+)
        lender1 = Lender(name="Match Lender", excluded_industries=["Gambling"])
        session.add(lender1)
        await session.flush()
        
        prog1 = LenderProgram(lender_id=lender1.id, program_name="Prime", tier_name="Tier A")
        session.add(prog1)
        await session.flush()
        
        session.add(LenderCriteria(program_id=prog1.id, criteria_type=CriteriaType.FICO_MIN, value_numeric=700))
        session.add(LenderCriteria(program_id=prog1.id, criteria_type=CriteriaType.TIB_MIN, value_numeric=2))
        
        # Lender 2: Fails (Excluded Industry)
        lender2 = Lender(name="Fail Industry", excluded_industries=["Construction"])
        session.add(lender2)
        await session.flush()
        
        # Lender 3: Fails (High FICO req)
        lender3 = Lender(name="Fail FICO", excluded_industries=[])
        session.add(lender3)
        await session.flush()
        
        prog3 = LenderProgram(lender_id=lender3.id, program_name="Super Prime", tier_name="Tier A+")
        session.add(prog3)
        await session.flush()
        
        session.add(LenderCriteria(program_id=prog3.id, criteria_type=CriteriaType.FICO_MIN, value_numeric=800))
        
        await session.commit()
        
        # 2. Run Match
        logger.info(f"Running match for Loan Request {loan.id}")
        results = await engine.evaluate_application(loan.id)
        
        # 3. Verify Results
        logger.info(f"Got {len(results)} match results.")
        
        for res in results:
            lender_name = (await session.execute(select(Lender.name).where(Lender.id == res.lender_id))).scalar()
            logger.info(f"Lender: {lender_name} | Eligible: {res.is_eligible} | Score: {res.fit_score}")
            if not res.is_eligible:
                logger.info(f"  Reasons: {res.rejection_reasons}")
                
        # Assertions
        passed = [r for r in results if r.is_eligible]
        failed = [r for r in results if not r.is_eligible]
        
        assert len(passed) >= 1, "Should have at least 1 passing lender"
        assert passed[0].fit_score > 0, "Passing lender should have positive score" 
        # Match Lender should pass
        
        logger.info("Verification Successful!")

        # Cleanup (optional, or rely on test DB reset)
        # await session.delete(business) ... cascading

if __name__ == "__main__":
    asyncio.run(verify_matching())
