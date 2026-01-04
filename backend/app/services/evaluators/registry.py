from app.models.lender import CriteriaType
from app.services.evaluators import *

EVALUATOR_REGISTRY = {
    CriteriaType.FICO_MIN: FICOEvaluator,
    CriteriaType.PAYNET_MIN: PayNetEvaluator,
    CriteriaType.TIB_MIN: TIBEvaluator,
    CriteriaType.REVENUE_MIN: RevenueEvaluator,
    CriteriaType.COMPARABLE_CREDIT_PERCENT: ComparableCreditEvaluator,
    CriteriaType.LOAN_AMOUNT_MIN: LoanAmountMinEvaluator,
    CriteriaType.LOAN_AMOUNT_MAX: LoanAmountMaxEvaluator,
    CriteriaType.MAX_EQUIPMENT_AGE: EquipmentAgeEvaluator,
    CriteriaType.INDUSTRY_EXCLUDED: IndustryEvaluator,
    # CriteriaType.INDUSTRY_ALLOWED: IndustryAllowedEvaluator, # Not implemented yet
    "STATE_EXCLUDED": StateEvaluator, # Custom key logic in engine needed or update Enum
}
