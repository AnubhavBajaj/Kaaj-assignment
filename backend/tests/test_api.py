import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.business import IndustryType
from app.models.lender import CriteriaType

# Fixture for async client
@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_application(client):
    app_payload = {
        "business": {
            "legal_name": f"Pytest Biz {uuid.uuid4()}",
            "industry": IndustryType.TECHNOLOGY.value,
            "state": "CA",
            "years_in_business": 5,
            "annual_revenue": 1000000
        },
        "guarantors": [
            {
                "first_name": "Test",
                "last_name": "Guarantor",
                "fico_score": 720,
                "ownership_percentage": 100
            }
        ],
        "loan_request": {
            "amount": 50000,
            "term_months": 36,
            "equipment_type": "Server",
            "equipment_cost": 50000
        }
    }
    resp = await client.post("/api/applications/", json=app_payload)
    assert resp.status_code == 201
    assert "application_id" in resp.json()
    assert resp.json()["status"] == "DRAFT"
    
    # Test List
    list_resp = await client.get("/api/applications/")
    assert list_resp.status_code == 200
    assert isinstance(list_resp.json(), list)
    assert len(list_resp.json()) >= 1
    
    return resp.json()["application_id"]

@pytest.mark.asyncio
async def test_lender_workflow(client):
    # Create Lender
    lender_payload = {
        "name": f"Pytest Lender {uuid.uuid4()}",
        "is_active": True,
        "excluded_states": [],
        "programs": [
            {
                "program_name": "Standard",
                "tier_name": "A",
                "criteria": [
                    {
                        "criteria_type": CriteriaType.FICO_MIN.value,
                        "value_numeric": 680
                    }
                ]
            }
        ]
    }
    resp = await client.post("/api/lenders/", json=lender_payload)
    assert resp.status_code == 201
    lender_id = resp.json()["id"]
    
    # We ideally need an app ID to test underwriting. 
    # Since tests run isolated/concurrently, we create a fresh app here or use a shared fixture.
    # For now, let's just create a quick app inside this test or depend on order (bad practice).
    # I'll create a fresh app here to be safe.
    
    app_payload = {
        "business": {
            "legal_name": f"Underwriting Test {uuid.uuid4()}",
            "industry": IndustryType.CONSTRUCTION.value,
            "state": "TX",
            "years_in_business": 3,
            "annual_revenue": 500000
        },
        "guarantors": [{"first_name":"G","last_name":"T","fico_score":700,"ownership_percentage":100}],
        "loan_request": {"amount":20000,"term_months":24,"equipment_type":"Tool","equipment_cost":20000}
    }
    app_resp = await client.post("/api/applications/", json=app_payload)
    app_id = app_resp.json()["application_id"]
    
    # Run Underwriting
    run_resp = await client.post(f"/api/underwriting/run/{app_id}")
    assert run_resp.status_code == 200
    assert run_resp.json()["status"] == "completed"
    
    # Check Results
    results_resp = await client.get(f"/api/underwriting/results/{app_id}")
    assert results_resp.status_code == 200
    results = results_resp.json()
    assert isinstance(results, list)
    # We expect at least one match if criteria met. 
    # Logic: FICO 700 >= 680. Should pass.
    # Note: verify_matching has other lenders in DB? Test db uses same as dev db in this setup usually.
    # If so, existing lenders might match too.
