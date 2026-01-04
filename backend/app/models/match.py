import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy import Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.loan import LoanRequest
    from app.models.lender import Lender, LenderProgram

class MatchResult(Base):
    __tablename__ = "match_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    loan_request_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("loan_requests.id"), nullable=False, index=True)
    lender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lenders.id"), nullable=False, index=True)
    program_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("lender_programs.id"), nullable=True, index=True)
    is_eligible: Mapped[bool] = mapped_column(Boolean, default=False)
    fit_score: Mapped[int] = mapped_column(Integer, default=0)
    rejection_reasons: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    criteria_details: Mapped[Optional[Any]] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    loan_request: Mapped["LoanRequest"] = relationship(back_populates="match_results")
    lender: Mapped["Lender"] = relationship(back_populates="match_results")
    program: Mapped[Optional["LenderProgram"]] = relationship(back_populates="match_results")
