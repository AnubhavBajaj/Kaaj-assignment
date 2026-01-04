import asyncio
import os
import argparse
import logging
from app.database import AsyncSessionLocal
from app.services.pdf_parser import extract_text_from_pdf
from app.services.policy_parser import PolicyParser
from app.services.policy_loader import PolicyLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def load_policies(pdf_dir: str):
    """
    Scans the given directory for PDFs, parses them, and loads them into the DB.
    """
    if not os.path.exists(pdf_dir):
        logger.error(f"Directory not found: {pdf_dir}")
        return

    async with AsyncSessionLocal() as session:
        loader = PolicyLoader(session)
        parser = PolicyParser()

        for filename in os.listdir(pdf_dir):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join(pdf_dir, filename)
                logger.info(f"Processing {filename}...")
                
                try:
                    # 1. Extract Text
                    text = extract_text_from_pdf(file_path)
                    
                    # 2. Parse Policy
                    # Heuristic: use filename as lender name hint or try to detect from text
                    # For now, let's assume filename starts with lender name or we pass it to parser
                    # The parser currently decides based on "lender_name" argument.
                    # We can try to infer it from the filename.
                    lender_name_hint = filename.replace(".pdf", "").replace("_", " ")
                    
                    parsed_data = parser.parse_policy(lender_name_hint, text)
                    
                    if "error" in parsed_data:
                        logger.warning(f"Could not parse {filename}: {parsed_data['error']}")
                        continue

                    # 3. Load into DB
                    await loader.load_lender_from_parsed_data(parsed_data)
                    
                except Exception as e:
                    logger.error(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load lender policies from PDFs.")
    parser.add_argument("--pdf-dir", required=True, help="Directory containing lender PDFs")
    
    args = parser.parse_args()
    
    asyncio.run(load_policies(args.pdf_dir))
