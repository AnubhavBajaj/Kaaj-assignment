from typing import Any, Dict
from app.services.evaluators.base import BaseEvaluator, EvaluationResult
from app.models.lender import CriteriaType

class FICOEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.FICO_MIN

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        guarantors = application_data.get("guarantors", [])
        if not guarantors:
            return EvaluationResult(passed=False, reason="No guarantors found", score_impact=-100)
        
        # Use max FICO of all guarantors
        max_fico = max((g.fico_score for g in guarantors), default=0)
        
        min_required = float(criteria_value)
        if max_fico >= min_required:
            score = 0
            if max_fico >= min_required + 50:
                 score = 5 # Bonus for excellent credit
            return EvaluationResult(passed=True, reason=f"FICO {max_fico} >= {min_required}", score_impact=score)
        else:
            return EvaluationResult(passed=False, reason=f"FICO {max_fico} < {min_required}", score_impact=-40)

class PayNetEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.PAYNET_MIN

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        credit = application_data.get("credit_profile")
        paynet = credit.paynet_score if credit and credit.paynet_score else 0
        
        min_required = float(criteria_value)
        
        if paynet == 0:
             # Some lenders might reject 0 paynet, others might ignore. 
             # Assuming fail if min is set and we have 0.
             return EvaluationResult(passed=False, reason="No PayNet score available", score_impact=-40)

        if paynet >= min_required:
            return EvaluationResult(passed=True, reason=f"PayNet {paynet} >= {min_required}", score_impact=0)
        else:
            return EvaluationResult(passed=False, reason=f"PayNet {paynet} < {min_required}", score_impact=-40)

class TIBEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.TIB_MIN

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        business = application_data.get("business")
        tib = business.years_in_business if business else 0
        
        min_required = float(criteria_value)
        
        if tib >= min_required:
             return EvaluationResult(passed=True, reason=f"TIB {tib} >= {min_required} years", score_impact=0)
        else:
             # Minor failure
             return EvaluationResult(passed=False, reason=f"TIB {tib} < {min_required} years", score_impact=-20)

class RevenueEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.REVENUE_MIN

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        business = application_data.get("business")
        revenue = float(business.annual_revenue) if business else 0.0
        
        min_required = float(criteria_value)
        
        if revenue >= min_required:
             return EvaluationResult(passed=True, reason=f"Revenue ${revenue:,.2f} >= ${min_required:,.2f}", score_impact=0)
        else:
             return EvaluationResult(passed=False, reason=f"Revenue ${revenue:,.2f} < ${min_required:,.2f}", score_impact=-30)

class ComparableCreditEvaluator(BaseEvaluator):
    CRITERIA_TYPE = CriteriaType.COMPARABLE_CREDIT_PERCENT

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        credit = application_data.get("credit_profile")
        loan = application_data.get("loan_request")
        
        if not credit or not loan:
             return EvaluationResult(passed=False, reason="Missing data", score_impact=-10)

        comparable_amt = float(credit.comparable_credit_amount)
        requested_amt = float(loan.amount)
        
        required_percent = float(criteria_value) # e.g. 50%
        required_amt = requested_amt * (required_percent / 100.0)
        
        if comparable_amt >= required_amt:
             return EvaluationResult(passed=True, reason=f"Comp Credit ${comparable_amt:,.2f} >= {required_percent}% of request", score_impact=0)
        
        return EvaluationResult(passed=False, reason=f"Comp Credit ${comparable_amt:,.2f} < {required_percent}% of request", score_impact=-30)
