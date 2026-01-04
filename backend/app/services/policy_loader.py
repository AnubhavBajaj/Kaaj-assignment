from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.models.lender import Lender, LenderProgram, LenderCriteria, CriteriaType
import logging

logger = logging.getLogger(__name__)

class PolicyLoader:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def load_lender_from_parsed_data(self, parsed_data: dict):
        """
        Loads parsed lender data into the database.
        Updates existing lender if found by name.
        """
        if "error" in parsed_data:
            logger.error(f"Skipping loading due to parse error: {parsed_data['error']}")
            return

        lender_name = parsed_data.get("lender_name")
        if not lender_name:
            logger.error("No lender name found in parsed data.")
            return

        try:
            # Check if lender exists
            stmt = select(Lender).where(Lender.name == lender_name).options(selectinload(Lender.programs))
            result = await self.session.execute(stmt)
            lender = result.scalars().first()

            if lender:
                logger.info(f"Updating existing lender: {lender_name}")
                # Clear existing programs to replace with new ones (simple update strategy)
                # In a real app, you might want to diff/update carefully.
                lender.excluded_industries = parsed_data.get("excluded_industries", [])
                lender.excluded_states = parsed_data.get("excluded_states", [])
                
                # Delete existing programs and criteria properly
                # First get program IDs to delete criteria
                prog_ids_stmt = select(LenderProgram.id).where(LenderProgram.lender_id == lender.id)
                prog_ids = (await self.session.execute(prog_ids_stmt)).scalars().all()
                
                if prog_ids:
                    await self.session.execute(delete(LenderCriteria).where(LenderCriteria.program_id.in_(prog_ids)))
                    await self.session.execute(delete(LenderProgram).where(LenderProgram.lender_id == lender.id))
            else:
                logger.info(f"Creating new lender: {lender_name}")
                lender = Lender(
                    name=lender_name,
                    excluded_industries=parsed_data.get("excluded_industries", []),
                    excluded_states=parsed_data.get("excluded_states", [])
                )
                self.session.add(lender)
                await self.session.flush() # Get ID

            # Create Programs and Criteria
            for prog_data in parsed_data.get("programs", []):
                program = LenderProgram(
                    lender_id=lender.id,
                    program_name=prog_data["program_name"],
                    tier_name=prog_data["tier_name"],
                    is_medical_program=prog_data.get("is_medical", False),
                    is_corporate_only=prog_data.get("is_corporate_only", False)
                )
                self.session.add(program)
                await self.session.flush()

                for param in prog_data.get("criteria", []):
                    criteria = LenderCriteria(
                        program_id=program.id,
                        criteria_type=param["type"],
                        value_numeric=param.get("value_numeric"),
                        value_text=param.get("value_text"),
                        value_boolean=param.get("value_boolean")
                    )
                    self.session.add(criteria)
            
            await self.session.commit()
            logger.info(f"Successfully loaded policy for {lender_name}")

        except Exception as e:
            logger.error(f"Failed to load policy for {lender_name}: {e}")
            await self.session.rollback()
            raise
