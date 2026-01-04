"""Pydantic v2 schemas for request/response validation."""

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


# Import schemas here as they are created
# from app.schemas.user import UserCreate, UserResponse
# from app.schemas.loan import LoanApplicationCreate, LoanApplicationResponse
# from app.schemas.document import DocumentUpload, DocumentResponse

__all__ = ["BaseSchema"]
