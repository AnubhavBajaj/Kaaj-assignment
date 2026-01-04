import asyncio
import asyncpg
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/loan_underwriting"
)

# Extract connection info to connect to default 'postgres' db
# Assuming standard format
from urllib.parse import urlparse

def get_postgres_url(url):
    parsed = urlparse(url)
    # Replace path (db name) with 'postgres'
    return url.replace(parsed.path, "/postgres")

async def create_database():
    target_db = "loan_underwriting"
    print(f"Checking if database '{target_db}' exists...")
    
    # Connect to default 'postgres' database
    # We need to strip asyncpg/driver info if present or just construct raw string for asyncpg
    # DATABASE_URL in config might be "postgresql+asyncpg://..."
    # asyncpg.connect expects "postgresql://..."
    
    db_url = DATABASE_URL
    if "postgresql+asyncpg" in db_url:
        db_url = db_url.replace("postgresql+asyncpg", "postgresql")
        
    admin_url = get_postgres_url(db_url)
    
    try:
        conn = await asyncpg.connect(admin_url)
    except Exception as e:
        print(f"Failed to connect to postgres: {e}")
        return

    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", target_db)
        if not exists:
            print(f"Database '{target_db}' does not exist. Creating...")
            await conn.execute(f'CREATE DATABASE "{target_db}"')
            print(f"Database '{target_db}' created successfully.")
        else:
            print(f"Database '{target_db}' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(create_database())
