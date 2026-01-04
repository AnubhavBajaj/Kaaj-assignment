import asyncio
import logging
from app.database import AsyncSessionLocal
from app.services.policy_parser import PolicyParser
from app.services.policy_loader import PolicyLoader
from sqlalchemy import select, func
from app.models.lender import Lender, LenderProgram

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_mock_loading():
    """
    Simulates loading policies from parsed text without needing actual PDFs.
    """
    logger.info("Starting mock verification...")
    
    async with AsyncSessionLocal() as session:
        loader = PolicyLoader(session)
        parser = PolicyParser()

        # Mock Data for Stearns Bank
        stearns_text = """
        Stearns Bank N.A.
        Standard Program Details:
        Min FICO: 700
        Min PayNet: 650
        Time in Business: 2 years
        Excluded Industries:
        - Cannabis
        - Gambling
        """
        
        # Mock Data for Apex
        apex_text = """
        Apex Commercial Capital
        Credit Guidelines
        A Credit: 650+ FICO, 2 Years TIB
        Restricted States: CA, NV, ND, VT
        """

        mock_pdfs = [
            ("Stearns Bank.pdf", stearns_text),
            ("Apex Commercial Capital.pdf", apex_text)
        ]

        for filename, text in mock_pdfs:
            logger.info(f"Processing mock file: {filename}")
            lender_name_hint = filename.replace(".pdf", "").replace("_", " ")
            
            # Parse
            parsed_data = parser.parse_policy(lender_name_hint, text)
            if "error" in parsed_data:
                logger.error(f"Parse error: {parsed_data['error']}")
                continue
            
            logger.info(f"Parsed data: {parsed_data}")

            # Load
            await loader.load_lender_from_parsed_data(parsed_data)
        
        # Verify in DB
        logger.info("Verifying database records...")
        
        lenders = (await session.execute(select(Lender))).scalars().all()
        logger.info(f"Total Lenders: {len(lenders)}")
        for l in lenders:
            programs = (await session.execute(select(LenderProgram).where(LenderProgram.lender_id == l.id))).scalars().all()
            logger.info(f"Lender: {l.name}")
            logger.info(f" - Excluded States: {l.excluded_states}")
            logger.info(f" - Programs: {len(programs)}")
            for p in programs:
                logger.info(f"   - Program: {p.program_name} ({p.tier_name})")

if __name__ == "__main__":
    asyncio.run(verify_mock_loading())
