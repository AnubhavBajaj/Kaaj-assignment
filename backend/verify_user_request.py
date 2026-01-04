import sys
import os
import asyncio
# Add parent dir to path if needed, though running as module is better
sys.path.append(os.getcwd())

from app.services.pdf_parser import extract_text_from_pdf
from app.services.policy_parser import parse_stearns_bank, PolicyParser
from app.cli.load_policies import load_policies

async def run_verification():
    print("1. Testing PDF parsing...")
    pdf_path = "./lender_pdfs/EF Credit Box 4.14.2025.pdf"
    if not os.path.exists(pdf_path):
        print(f"Warning: {pdf_path} not found. Ensure create_test_pdfs.py ran successfully.")
        return

    text = extract_text_from_pdf(pdf_path)
    print(f"Text length: {len(text)}")
    print(f"Preview: {text[:100]}...")
    
    print("\n2. Testing policy parsing...")
    policies = parse_stearns_bank(text)
    print(f"Lender: {policies.get('lender_name')}")
    tiers = policies.get('programs', [])
    print(f"Programs found: {len(tiers)}")
    if tiers:
        print(f"First Program: {tiers[0].get('program_name')}")
        print(f"Criteria count: {len(tiers[0].get('criteria', []))}")

    print("\n3. Loading all lenders...")
    # Clean up DB for lenders first? 
    # The loader updates existing ones, so it's fine.
    await load_policies("./lender_pdfs")
    print("Loading complete.")

    print("\n4. Verifying in database...")
    from sqlalchemy import text
    from app.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        # Expected: All 5 lenders with program counts
        # SELECT l.name, COUNT(p.id) as programs FROM lenders l LEFT JOIN lender_programs p ON l.id = p.lender_id GROUP BY l.name;
        stmt = text("SELECT l.name, COUNT(p.id) as programs FROM lenders l LEFT JOIN lender_programs p ON l.id = p.lender_id GROUP BY l.name")
        result = await session.execute(stmt)
        rows = result.fetchall()
        print("Lender Name | Program Count")
        print("-" * 30)
        for row in rows:
            print(f"{row[0]} | {row[1]}")

if __name__ == "__main__":
    asyncio.run(run_verification())

