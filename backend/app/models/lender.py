import uuid
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Integer, Boolean, ForeignKey, Enum as SAEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.match import MatchResult

class CriteriaType(str, Enum):
    FICO_MIN = "FICO_MIN"
    PAYNET_MIN = "PAYNET_MIN"
    TIB_MIN = "TIB_MIN"
    LOAN_AMOUNT_MIN = "LOAN_AMOUNT_MIN"
    LOAN_AMOUNT_MAX = "LOAN_AMOUNT_MAX"
    REVENUE_MIN = "REVENUE_MIN"
    INDUSTRY_ALLOWED = "INDUSTRY_ALLOWED"
    INDUSTRY_EXCLUDED = "INDUSTRY_EXCLUDED"

class Lender(Base):
    __tablename__ = "lenders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    excluded_states: Mapped[List[str]] = mapped_column(ARRAY(String), default=list)
    excluded_industries: Mapped[List[str]] = mapped_column(ARRAY(String), default=list)
    excluded_equipment_types: Mapped[List[str]] = mapped_column(ARRAY(String), default=list)

    # Relationships
    programs: Mapped[List["LenderProgram"]] = relationship(back_populates="lender", cascade="all, delete-orphan")
    match_results: Mapped[List["MatchResult"]] = relationship(back_populates="lender")

class LenderProgram(Base):
    __tablename__ = "lender_programs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lender_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lenders.id"), nullable=False, index=True)
    program_name: Mapped[str] = mapped_column(String, nullable=False)
    tier_name: Mapped[str] = mapped_column(String, nullable=False)
    is_medical_program: Mapped[bool] = mapped_column(Boolean, default=False)
    is_corporate_only: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    lender: Mapped["Lender"] = relationship(back_populates="programs")
    criteria: Mapped[List["LenderCriteria"]] = relationship(back_populates="program", cascade="all, delete-orphan")
    match_results: Mapped[List["MatchResult"]] = relationship(back_populates="program")

class LenderCriteria(Base):
    __tablename__ = "lender_criteria"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("lender_programs.id"), nullable=False, index=True)
    criteria_type: Mapped[CriteriaType] = mapped_column(SAEnum(CriteriaType), nullable=False)
    value_numeric: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    value_text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    value_boolean: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)

    # Relationships
    program: Mapped["LenderProgram"] = relationship(back_populates="criteria")
