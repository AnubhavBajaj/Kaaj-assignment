import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Integer, Float, Boolean, ForeignKey, Numeric, Enum as SAEnum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base

if TYPE_CHECKING:
    from app.models.business import Business
    from app.models.match import MatchResult

class LoanStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    DELETED = "DELETED"

class LoanRequest(Base):
    __tablename__ = "loan_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    term_months: Mapped[int] = mapped_column(Integer, nullable=False)
    equipment_type: Mapped[str] = mapped_column(String, nullable=False)
    equipment_age_years: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    equipment_cost: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    soft_costs: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    is_private_party_sale: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[LoanStatus] = mapped_column(SAEnum(LoanStatus), default=LoanStatus.DRAFT, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    business: Mapped["Business"] = relationship(back_populates="loan_requests")
    match_results: Mapped[List["MatchResult"]] = relationship(back_populates="loan_request", cascade="all, delete-orphan")
