from typing import Any, Dict
from app.services.evaluators.base import BaseEvaluator, EvaluationResult
from app.models.lender import CriteriaType

class LoanAmountMinEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.LOAN_AMOUNT_MIN

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        loan = application_data.get("loan_request")
        amount = float(loan.amount) if loan else 0.0
        min_val = float(criteria_value)
        
        if amount >= min_val:
            return EvaluationResult(passed=True, reason=f"Amount ${amount:,.2f} >= min ${min_val:,.2f}", score_impact=0)
        return EvaluationResult(passed=False, reason=f"Amount ${amount:,.2f} too low (min ${min_val:,.2f})", score_impact=-50) # Strict fail usually

class LoanAmountMaxEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.LOAN_AMOUNT_MAX

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        loan = application_data.get("loan_request")
        amount = float(loan.amount) if loan else 0.0
        max_val = float(criteria_value)
        
        if amount <= max_val:
            return EvaluationResult(passed=True, reason=f"Amount ${amount:,.2f} <= max ${max_val:,.2f}", score_impact=0)
        return EvaluationResult(passed=False, reason=f"Amount ${amount:,.2f} too high (max ${max_val:,.2f})", score_impact=-50)

class EquipmentAgeEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.MAX_EQUIPMENT_AGE

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        loan = application_data.get("loan_request")
        age = loan.equipment_age_years if loan and loan.equipment_age_years is not None else 0
        max_age = int(criteria_value)
        
        if age <= max_age:
             return EvaluationResult(passed=True, reason=f"Age {age} <= max {max_age} years", score_impact=0)
        return EvaluationResult(passed=False, reason=f"Equipment too old ({age} > {max_age} years)", score_impact=-30)
