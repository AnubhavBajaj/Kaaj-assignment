import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import String, Integer, Float, Boolean, Date, DateTime, ForeignKey, Enum as SAEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base

class IndustryType(str, Enum):
    RETAIL = "RETAIL"
    CONSTRUCTION = "CONSTRUCTION"
    TRANSPORTATION = "TRANSPORTATION"
    HEALTHCARE = "HEALTHCARE"
    HOSPITALITY = "HOSPITALITY"
    MANUFACTURING = "MANUFACTURING"
    TECHNOLOGY = "TECHNOLOGY"
    OTHER = "OTHER"

class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    legal_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    dba_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    industry: Mapped[IndustryType] = mapped_column(SAEnum(IndustryType), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    years_in_business: Mapped[float] = mapped_column(Float, nullable=False)
    annual_revenue: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationships
    guarantors: Mapped[List["PersonalGuarantor"]] = relationship(back_populates="business", cascade="all, delete-orphan")
    credit_profile: Mapped[Optional["BusinessCredit"]] = relationship(back_populates="business", uselist=False, cascade="all, delete-orphan")
    loan_requests: Mapped[List["LoanRequest"]] = relationship(back_populates="business")

class PersonalGuarantor(Base):
    __tablename__ = "personal_guarantors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False, index=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    fico_score: Mapped[int] = mapped_column(Integer, nullable=False)
    ownership_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    has_bankruptcy: Mapped[bool] = mapped_column(Boolean, default=False)
    bankruptcy_discharge_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    has_foreclosure: Mapped[bool] = mapped_column(Boolean, default=False)
    has_repossession: Mapped[bool] = mapped_column(Boolean, default=False)
    has_judgement: Mapped[bool] = mapped_column(Boolean, default=False)
    revolving_debt_balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    total_unsecured_debt: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    # Relationships
    business: Mapped["Business"] = relationship(back_populates="guarantors")

class BusinessCredit(Base):
    __tablename__ = "business_credits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("businesses.id"), nullable=False, unique=True)
    paynet_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    has_comparable_credit: Mapped[bool] = mapped_column(Boolean, default=False)
    comparable_credit_amount: Mapped[float] = mapped_column(Numeric(15, 2), default=0)
    open_trade_lines_count: Mapped[int] = mapped_column(Integer, default=0)
    has_collections: Mapped[bool] = mapped_column(Boolean, default=False)
    has_tax_liens: Mapped[bool] = mapped_column(Boolean, default=False)
    collections_charge_off_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Relationships
    business: Mapped["Business"] = relationship(back_populates="credit_profile")
