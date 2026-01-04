import asyncio
import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/loan_underwriting"
)

async def verify_tables():
    # Fix URL for asyncpg if needed
    db_url = DATABASE_URL
    if "postgresql+asyncpg" in db_url:
        db_url = db_url.replace("postgresql+asyncpg", "postgresql")
    
    print(f"Connecting to {db_url}...")
    try:
        conn = await asyncpg.connect(db_url)
    except Exception as e:
        print(f"Failed to connect: {e}")
        return

    try:
        # Query for tables
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        rows = await conn.fetch(query)
        print("\nExisting tables:")
        for row in rows:
            print(f"- {row['table_name']}")
            
        expected_tables = {
            "businesses", "personal_guarantors", "business_credits", 
            "loan_requests", "lenders", "lender_programs", 
            "lender_criteria", "match_results", "alembic_version"
        }
        
        found_tables = {row['table_name'] for row in rows}
        
        missing = expected_tables - found_tables
        if missing:
            print(f"\nMissing tables: {missing}")
        else:
            print("\nAll expected tables found.")
            
    except Exception as e:
        print(f"Error querying tables: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(verify_tables())
