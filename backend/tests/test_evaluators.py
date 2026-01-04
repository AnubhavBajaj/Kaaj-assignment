from app.services.evaluators.financial import FICOEvaluator, PayNetEvaluator, TIBEvaluator
from app.services.evaluators.loan import LoanAmountMinEvaluator, EquipmentAgeEvaluator
from app.services.evaluators.legal import IndustryEvaluator, StateEvaluator
from app.models.business import PersonalGuarantor, Business, BusinessCredit, IndustryType


# Mock Objects (using simple dataclasses or namedtuples if models are complex, but models are fine)
class MockGuarantor:
    def __init__(self, fico):
        self.fico_score = fico

class MockCredit:
    def __init__(self, paynet):
        self.paynet_score = paynet

class MockBusiness:
    def __init__(self, industry, state, tib):
        self.industry = industry
        self.state = state
        self.years_in_business = tib

class MockLoan:
    def __init__(self, amount, age):
        self.amount = amount
        self.equipment_age_years = age

def test_fico_evaluator():
    evaluator = FICOEvaluator()
    
    # Pass case
    app_data = {"guarantors": [MockGuarantor(700), MockGuarantor(650)]}
    result = evaluator.evaluate(app_data, 680)
    assert result.passed
    assert result.score_impact == 0
    
    # Fail case
    app_data = {"guarantors": [MockGuarantor(600)]}
    result = evaluator.evaluate(app_data, 680)
    assert not result.passed
    assert result.score_impact == -40

    # Bonus case
    app_data = {"guarantors": [MockGuarantor(750)]}
    result = evaluator.evaluate(app_data, 680)
    assert result.passed
    assert result.score_impact == 5

def test_paynet_evaluator():
    evaluator = PayNetEvaluator()
    
    app_data = {"credit_profile": MockCredit(700)}
    result = evaluator.evaluate(app_data, 650)
    assert result.passed
    
    app_data = {"credit_profile": MockCredit(600)}
    result = evaluator.evaluate(app_data, 650)
    assert not result.passed

def test_industry_evaluator():
    evaluator = IndustryEvaluator()
    
    # Pass: Industry not in excluded list
    app_data = {"business": MockBusiness("Construction", "TX", 5)}
    result = evaluator.evaluate(app_data, ["Gambling", "Cannabis"])
    assert result.passed
    
    # Fail: Industry in excluded list
    app_data = {"business": MockBusiness("Gambling", "TX", 5)}
    result = evaluator.evaluate(app_data, ["Gambling", "Cannabis"])
    assert not result.passed
    assert result.score_impact == -100

def test_state_evaluator():
    evaluator = StateEvaluator()
    
    # Pass
    app_data = {"business": MockBusiness("Retail", "NY", 5)}
    result = evaluator.evaluate(app_data, ["CA", "NV"])
    assert result.passed
    
    # Fail
    app_data = {"business": MockBusiness("Retail", "CA", 5)}
    result = evaluator.evaluate(app_data, ["CA", "NV"])
    assert not result.passed
    assert result.score_impact == -100
