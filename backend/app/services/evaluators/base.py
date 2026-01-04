from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Dict
from app.models.lender import CriteriaType

@dataclass
class EvaluationResult:
    passed: bool
    reason: str
    score_impact: int = 0

class BaseEvaluator(ABC):
    """
    Abstract base class for all criteria evaluators.
    """
    
    CRITERIA_TYPE: CriteriaType = None

    @abstractmethod
    def evaluate(self, application_data: Dict[str, Any], criteria_value: Any) -> EvaluationResult:
        """
        Evaluates the application data against the specific criteria value.
        
        Args:
            application_data: Dictionary containing all relevant application data 
                            (business, guarantors, loan_request, credit_profile)
            criteria_value: The value defined in the lender's criteria for this rule.
            
        Returns:
            EvaluationResult indicating pass/fail, reason, and score impact.
        """
        pass
