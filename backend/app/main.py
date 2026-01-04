"""FastAPI application entry point for the loan underwriting platform."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup: Try to create database tables (for development only)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Database connected successfully")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   The API will start, but database operations will fail.")
        print("   Start PostgreSQL with: docker compose up -d db")
    yield
    # Shutdown: Dispose of the engine
    try:
        await engine.dispose()
    except Exception:
        pass


app = FastAPI(
    title="Loan Underwriting Platform",
    description="API for loan application processing and underwriting",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://frontend:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "loan-underwriting-backend"}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Loan Underwriting Platform API",
        "docs": "/docs",
        "health": "/health",
    }
