from typing import Any, Dict
from app.services.evaluators.base import BaseEvaluator, EvaluationResult
from app.models.lender import CriteriaType

class IndustryEvaluator(BaseEvaluator):
    # This might handle both Allowed and Excluded via different logic or types
    # Here implementing for EXCLUDED as that's common on Lender level
    CRITERIA_TYPE = CriteriaType.INDUSTRY_EXCLUDED

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        # criteria_value here is likely a LIST of strings from the Lender model, 
        # but the abstract class usually takes a single criteria row value.
        # However, for Lender-level arrays (excluded_industries), we might handle differently 
        # or map them to a pseudo-criteria.
        
        # Let's assume the engine passes the list of excluded industries here.
        business = application_data.get("business")
        industry = business.industry if business else "OTHER"
        
        excluded_list = criteria_value if isinstance(criteria_value, list) else []
        
        # Check partial match or exact
        for excluded in excluded_list:
            if excluded.lower() in industry.lower():
                 return EvaluationResult(passed=False, reason=f"Industry '{industry}' is excluded ({excluded})", score_impact=-100)
        
        return EvaluationResult(passed=True, reason="Industry allowed", score_impact=0)

class StateEvaluator(BaseEvaluator):
    CRITERIA_TYPE = "STATE_EXCLUDED" # Custom key, not in CriteriaType enum yet but useful

    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        business = application_data.get("business")
        state = business.state if business else ""
        
        excluded_list = criteria_value if isinstance(criteria_value, list) else []
        
        if state in excluded_list:
             return EvaluationResult(passed=False, reason=f"State '{state}' is excluded", score_impact=-100)
        
        return EvaluationResult(passed=True, reason="State allowed", score_impact=0)
